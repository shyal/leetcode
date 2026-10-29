// mu as a language in LeetCode's editor. Runs in the page itself (it
// needs the page's `monaco`), and reaches the extension through
// mu_bridge.js; ask, register and OPENS_BLOCK come from mu_common.js.
//
// Choosing mu in the language menu sets LeetCode to Python3 and lays a
// second Monaco editor, holding the mu, over LeetCode's. LeetCode's own
// editor keeps its Python untouched while you type. Run and Submit (the
// buttons, Cmd+' and Cmd+Enter) are caught first: the mu compiles, the
// submission (the mu quoted as comments, then the Python) goes into
// LeetCode's editor, and the click goes through. The mu and the choice of
// mu are kept per problem.
//
// Contest pages have a CodeMirror editor and no Monaco. There the mu goes
// into LeetCode's own editor, and the submission replaces `typed_code` in
// the request that Run or Submit sends. That editor indents by Python's
// four spaces; with mu on, Tab, Shift+Tab, Enter and Backspace indent by
// mu's two.

(() => {
  const PROBLEM = /^(?:\/contest\/[^/]+)?\/problems\/([^/?#]+)/;
  const BUTTON = '[data-e2e-locator="console-run-button"],[data-e2e-locator="console-submit-button"]';
  const ROW = "div.group.cursor-pointer";
  const { OPENS_BLOCK, ask, register } = window.__mu;

  const slug = () => PROBLEM.exec(location.pathname)?.[1] || null;
  const pyEditor = () => window.monaco?.editor.getEditors().find((e) => e.getModel()?.getLanguageId() === "python3");
  // the contest editor: CodeMirror 6 keeps its view on the content node (the
  // test cases are CodeMirror editors too, outside the code editor's box)
  const cmView = () =>
    window.monaco ? null : document.querySelector('[data-track-load="code_editor"] .cm-content')?.cmView?.view || null;
  const cmPython = () => (cmView() && /^(Python3|mu)$/.test(langButton()?.firstChild.data) ? cmView() : null);
  const pyReady = () => pyEditor() || cmPython();
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  const label = (row) => row.textContent.trim();
  const cmText = (view) => view.state.doc.toString();
  const cmSet = (view, text) => view.dispatch({ changes: { from: 0, to: view.state.doc.length, insert: text } });

  let on = null; // {slug, editor, model, box, status}, or on a contest page {slug, view, status, text, py}
  let entering = false;
  let passing = false; // our own click on Run / Submit, let through

  // LeetCode's language button: its first child is the label text
  function langButton() {
    return [...document.querySelectorAll('button[aria-haspopup="dialog"]')].find(
      (b) => b.firstChild?.nodeType === 3 && /^(Python3|mu)$/.test(b.firstChild.data),
    );
  }
  function showLabel(text) {
    const b = langButton();
    if (b && b.firstChild.data !== text) b.firstChild.data = text;
  }

  function say(text, bad = false) {
    if (!on) return;
    on.status.textContent = text;
    on.status.style.color = bad ? "#ef6f61" : "";
  }

  async function check() {
    if (!on) return;
    if (on.view) return cmCheck();
    const { model } = on;
    const r = await ask("transpile", { src: model.getValue() });
    if (!on || on.model !== model) return;
    const line = r.ok ? 0 : Number(/^line (\d+)/.exec(r.error)?.[1] || 1);
    window.monaco.editor.setModelMarkers(model, "mu", r.ok ? [] : [{
      severity: window.monaco.MarkerSeverity.Error, message: r.error,
      startLineNumber: line, endLineNumber: line, startColumn: 1, endColumn: model.getLineMaxColumn(line),
    }]);
    say(r.ok ? "mu: Cmd+' runs, Cmd+Enter submits" : r.error, !r.ok);
  }

  async function cmCheck() {
    const mine = on;
    const r = await ask("transpile", { src: mine.text });
    if (on !== mine || mine.text !== cmText(mine.view)) return;
    if (r.ok) mine.py = r.value;
    say(r.ok ? "mu: Cmd+' runs, Cmd+Enter submits" : r.error, !r.ok);
  }

  // the contest page: the mu goes into LeetCode's own CodeMirror editor
  async function enterCm() {
    const view = cmPython();
    const s = slug();
    if (!view || !s || on || entering) return;
    entering = true;
    try {
      let text = await ask("get", { key: `mu:${s}` });
      if (!text) {
        const r = await ask("starter", { src: cmText(view) });
        text = r.ok ? r.value : "";
      }
      const host = view.dom.parentElement?.parentElement || view.dom;
      if (!text) {
        cmAlert(host, "mu cannot write this one: it has no class Solution.");
        return;
      }
      if (cmText(view) !== text) cmSet(view, text);
      if (getComputedStyle(host).position === "static") host.style.position = "relative";
      const status = document.createElement("div");
      status.style.cssText = "position:absolute;right:0;bottom:0;z-index:20;max-width:100%;padding:2px 8px;" +
        "font:12px system-ui,sans-serif;opacity:.8;color:#aaa;pointer-events:none;white-space:pre-wrap;";
      host.append(status);
      on = { slug: s, view, status, text, py: null, sending: null };
      ask("set", { key: `mu:on:${s}`, value: true });
      showLabel("mu");
      check();
      view.focus();
    } finally {
      entering = false;
    }
  }

  function cmAlert(host, text) {
    const bar = document.createElement("div");
    bar.textContent = text;
    bar.style.cssText = "position:absolute;left:0;right:0;bottom:0;z-index:20;padding:4px 8px;" +
      "font:12px system-ui,sans-serif;background:#5a1d1d;color:#fff;";
    host.append(bar);
    setTimeout(() => bar.remove(), 4000);
  }

  async function enter() {
    if (cmPython()) return enterCm();
    const py = pyEditor();
    const s = slug();
    if (!py || !s || on || entering) return;
    entering = true;
    try {
      let text = await ask("get", { key: `mu:${s}` });
      if (!text) {
        const r = await ask("starter", { src: py.getValue() });
        text = r.ok ? r.value : "";
      }
      if (!text) {
        alertBar(py, "mu cannot write this one: it has no class Solution.");
        return;
      }
      register();
      const host = py.getContainerDomNode();
      const box = document.createElement("div");
      box.style.cssText = "position:absolute;inset:0;z-index:20;display:flex;flex-direction:column;";
      const bg = getComputedStyle(host.querySelector(".monaco-editor-background") || host).backgroundColor;
      const pane = document.createElement("div");
      pane.style.cssText = "flex:1;min-height:0;";
      const status = document.createElement("div");
      status.style.cssText = `padding:2px 8px;font:12px system-ui,sans-serif;opacity:.8;background:${bg};color:#aaa;`;
      box.append(pane, status);
      host.append(box);
      const raw = py.getRawOptions();
      const model = window.monaco.editor.createModel(text, "mu");
      const editor = window.monaco.editor.create(pane, {
        model, automaticLayout: true, fontSize: raw.fontSize, fontFamily: raw.fontFamily,
        lineHeight: raw.lineHeight, tabSize: 2, insertSpaces: true, detectIndentation: false,
        minimap: { enabled: false }, scrollBeyondLastLine: false,
      });
      const { KeyMod, KeyCode } = window.monaco;
      editor.addCommand(KeyMod.CtrlCmd | KeyCode.Enter, () => press("submit"));
      editor.addCommand(KeyMod.CtrlCmd | KeyCode.Quote, () => press("run"));
      on = { slug: s, editor, model, box, status };
      let saving = null;
      model.onDidChangeContent(() => {
        clearTimeout(saving);
        saving = setTimeout(() => {
          ask("set", { key: `mu:${s}`, value: model.getValue() });
          check();
        }, 300);
      });
      ask("set", { key: `mu:on:${s}`, value: true });
      showLabel("mu");
      check();
      editor.focus();
    } finally {
      entering = false;
    }
  }

  function leave(forget = true) {
    if (!on) return;
    if (forget) ask("set", { key: `mu:on:${on.slug}`, value: false });
    if (on.view) {
      // Python3 gets the compiled mu back, not the mu itself
      if (forget && on.py && on.view.dom.isConnected) cmSet(on.view, on.py);
      on.status.remove();
    } else {
      on.editor.dispose();
      on.model.dispose();
      on.box.remove();
    }
    on = null;
    showLabel("Python3");
  }

  // a one-line message over LeetCode's editor, gone after a few seconds
  function alertBar(py, text) {
    const bar = document.createElement("div");
    bar.textContent = text;
    bar.style.cssText = "position:absolute;left:0;right:0;bottom:0;z-index:20;padding:4px 8px;" +
      "font:12px system-ui,sans-serif;background:#5a1d1d;color:#fff;";
    py.getContainerDomNode().append(bar);
    setTimeout(() => bar.remove(), 4000);
  }

  function press(which) {
    document.querySelector(`[data-e2e-locator="console-${which}-button"]`)?.click();
  }

  // Run / Submit while mu is on: compile, fill LeetCode's editor, then click
  document.addEventListener("click", async (e) => {
    const button = e.target.closest?.(BUTTON);
    if (!on || passing || !button) return;
    e.preventDefault();
    e.stopImmediatePropagation();
    const r = await ask("submission", { src: on.view ? cmText(on.view) : on.model.getValue() });
    if (!on) return;
    if (!r.ok) return say(r.error, true);
    if (on.view) {
      on.sending = r.value; // the request's typed_code, swapped below
    } else {
      pyEditor()?.getModel().setValue(r.value);
      await sleep(150); // LeetCode reads the editor through its change events
    }
    passing = true;
    try {
      button.click();
    } finally {
      passing = false;
    }
    on?.editor?.focus();
  }, true);

  // on a contest page Run and Submit send the editor's text, the mu: the
  // request carries the compiled submission instead
  const SENDS = /\/(interpret_solution|submit)\/?$/;
  const fetch0 = window.fetch;
  window.fetch = function (input, init) {
    const url = typeof input === "string" ? input : input?.url || "";
    const path = url && new URL(url, location.href).pathname;
    if (on?.view && on.sending && SENDS.test(path) && typeof init?.body === "string") {
      try {
        const body = JSON.parse(init.body);
        if ("typed_code" in body) {
          body.typed_code = on.sending;
          body.lang = "python3";
          init = { ...init, body: JSON.stringify(body) };
        }
      } catch {
        // not JSON: sent as it is
      }
    }
    return fetch0.call(this, input, init);
  };

  // LeetCode's own shortcuts would send the Python under the mu
  window.addEventListener("keydown", (e) => {
    if (!on || !(e.metaKey || e.ctrlKey)) return;
    const which = e.key === "Enter" ? "submit" : e.key === "'" ? "run" : null;
    if (!which) return;
    e.preventDefault();
    e.stopImmediatePropagation();
    press(which);
  }, true);

  // the contest editor is LeetCode's, set to Python's four spaces: with mu
  // on, Tab, Shift+Tab, Enter and Backspace indent by two
  const STEP = 2;
  window.addEventListener("keydown", (e) => {
    if (!on?.view || e.metaKey || e.ctrlKey || e.altKey || !on.view.contentDOM.contains(e.target)) return;
    const { state } = on.view;
    const { from, to } = state.selection.main;
    const line = state.doc.lineAt(from);
    const col = from - line.from;
    const lead = line.text.length - line.text.trimStart().length;
    let tr = null;
    if (e.key === "Tab" && !e.shiftKey && from === to) {
      const insert = " ".repeat(STEP - (col % STEP));
      tr = { changes: { from, insert }, selection: { anchor: from + insert.length } };
    } else if (e.key === "Tab") {
      // every line the selection touches moves one step; the selection follows
      const changes = [];
      for (let n = line.number; n <= state.doc.lineAt(to).number; n++) {
        const l = state.doc.line(n);
        if (!e.shiftKey) {
          changes.push({ from: l.from, insert: " ".repeat(STEP) });
        } else {
          const spaces = l.text.length - l.text.trimStart().length;
          const cut = Math.min(spaces, spaces % STEP || STEP);
          if (cut) changes.push({ from: l.from, to: l.from + cut });
        }
      }
      if (!changes.length) return;
      tr = { changes };
    } else if (e.key === "Enter") {
      const before = line.text.slice(0, col);
      const indent = " ".repeat(Math.min(lead, col) + (OPENS_BLOCK.test(before) ? STEP : 0));
      const insert = "\n" + indent;
      tr = { changes: { from, to, insert }, selection: { anchor: from + insert.length } };
    } else if (e.key === "Backspace" && from === to && col > 0 && col <= lead) {
      tr = { changes: { from: from - (col % STEP || STEP), to: from } };
    }
    if (!tr) return;
    e.preventDefault();
    e.stopImmediatePropagation();
    on.view.dispatch({ ...tr, scrollIntoView: true, userEvent: e.key === "Backspace" ? "delete" : "input" });
  }, true);

  // the language menu: a mu row under Python3, and leaving mu on any other choice
  function addRow(menu) {
    const rows = [...menu.querySelectorAll(ROW)];
    const py3 = rows.find((r) => label(r) === "Python3");
    const py2 = rows.find((r) => label(r) === "Python");
    if (!py3 || !py2 || menu.querySelector("[data-mu-row]")) return;
    const row = py2.cloneNode(true);
    row.dataset.muRow = "1";
    row.querySelector(".text-sm").textContent = "mu";
    row.lastElementChild?.remove(); // the hover icon: LeetCode's, for its own languages
    const tick = (r, shown) => {
      const svg = r.querySelector("svg");
      svg?.classList.toggle("visible", shown);
      svg?.classList.toggle("invisible", !shown);
    };
    tick(row, !!on);
    if (on) tick(py3, false);
    py3.after(row);
    row.addEventListener("click", async (e) => {
      e.stopPropagation();
      if (pyReady()) {
        document.dispatchEvent(new KeyboardEvent("keydown", { key: "Escape", bubbles: true }));
      } else {
        py3.click(); // LeetCode switches to Python3 and closes the menu
        for (let i = 0; i < 30 && !pyReady(); i++) await sleep(100);
        await sleep(200); // CodeMirror gets the Python3 code a moment after the label
      }
      enter();
    });
    menu.addEventListener("click", (e) => {
      const r = e.target.closest(ROW);
      if (r && !r.dataset.muRow) leave();
    }, true);
  }

  // every tick: the menu, a new problem, a rebuilt editor, a label React reset
  let seen = null;
  async function tick() {
    for (const menu of document.querySelectorAll('[role="dialog"]')) addRow(menu);
    const s = slug();
    if (on && (s !== on.slug || !(on.view ? on.view.dom : on.box).isConnected)) {
      leave(false);
      seen = null; // a rebuilt editor on the same problem gets the mu back
    }
    if (on?.view && cmText(on.view) !== on.text) {
      on.text = cmText(on.view);
      ask("set", { key: `mu:${on.slug}`, value: on.text });
      check();
    }
    if (on) showLabel("mu");
    if (s && !on && !entering && pyReady() && seen !== s) {
      seen = s;
      if (await ask("get", { key: `mu:on:${s}` })) enter();
    }
    if (!s) seen = null;
  }

  const start = () => {
    new MutationObserver(() => requestAnimationFrame(tick)).observe(document.body, { childList: true, subtree: true });
    setInterval(tick, 1000);
  };
  if (document.body) start();
  else document.addEventListener("DOMContentLoaded", start);
})();
