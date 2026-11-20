// mu as a language in aced.io's editor: the practice page (a live
// session with a peer), the pages that prepare a question, and the
// question pages. Runs in the page itself (it needs the page's `monaco`);
// ask, register and OPENS_BLOCK come from mu_common.js.
//
// The language menu gets two mu options, one for what the peer sees:
//
// "mu, share Python": a second Monaco editor, holding the mu, takes the
// left half and aced's editor the right half. Each change compiles, and
// the Python goes into aced's editor at once: the peer sees Python as it
// is written, and so does the writer, beside the mu. The Python lines
// that come from the mu line under the cursor are marked. Run code (the
// button, or Cmd+Enter in the mu) and Run tests run that Python.
//
// "mu, share mu": the mu is written in aced's own editor, so the peer
// sees it and can edit it. Run code (the button or Cmd+Enter) and Run
// tests put the Python in the editor for the moment aced reads it, then
// the mu comes back.
//
// The mu and the choice of mode are kept per page.
//
// The script is on every aced.io page: aced moves between its pages
// without a page load, so a session or a question is often reached from
// a page that has no editor.

(() => {
  const { ask, register } = window.__mu;
  // a session id, a question's number, or prepare/<question>: each question prepared is its own page
  const PAGE = /^\/(practice|questions)\/((?:prepare\/)?[^/?#]+)/;
  const MODES = { python: "mu, share Python", mu: "mu, share mu" }; // mode -> its line in the menu
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

  const pageId = () => {
    const m = PAGE.exec(location.pathname);
    return m ? `${m[1]}/${m[2]}` : null;
  };
  let on = null; // {id, share, py, model, status, saved} and, sharing Python: {editor, box, marks, origin}
  let entering = false;
  let saving = null;
  let swapping = false; // the Python is in aced's editor for a run: its changes are not the writer's

  // aced's editor: the one that is not ours, in Python (or in mu while the mu is shared)
  const acedEditor = () =>
    window.monaco?.editor.getEditors().find((e) => e !== on?.editor && /^(python|mu)$/.test(e.getModel()?.getLanguageId() || ""));
  // aced's language menu: a native select, transparent, over a button that shows the label
  const langSelect = () =>
    [...document.querySelectorAll("select")].find((s) => [...s.options].some((o) => o.value === "python")) || null;
  const runButton = () => [...document.querySelectorAll("button")].find((b) => b.textContent.trim().startsWith("Run code"));
  const muModel = () => (on?.share === "python" ? on.model : on?.py.getModel());

  function say(text, bad = false) {
    if (!on) return;
    on.status.textContent = text;
    on.status.style.color = bad ? "#c0392b" : "#777";
  }

  // a line across the foot of an editor's box
  function foot(host, text = "") {
    const bg = getComputedStyle(host.querySelector(".monaco-editor-background") || host).backgroundColor;
    const bar = document.createElement("div");
    bar.textContent = text;
    bar.style.cssText = `padding:2px 8px;font:12px system-ui,sans-serif;background:${bg};color:#777;`;
    return bar;
  }

  // the mu compiled: {ok, py, origin} or {ok: false, error}; the mu's
  // errors are marked on its model
  async function compiled(model) {
    const r = await ask("shared", { src: model.getValue() });
    const line = r.ok ? 0 : Math.min(Number(/^line (\d+)/.exec(r.error)?.[1] || 1), model.getLineCount());
    if (!model.isDisposed()) {
      window.monaco.editor.setModelMarkers(model, "mu", r.ok ? [] : [{
        severity: window.monaco.MarkerSeverity.Error, message: r.error,
        startLineNumber: line, endLineNumber: line, startColumn: 1, endColumn: model.getLineMaxColumn(line),
      }]);
    }
    return r.ok ? { ok: true, ...JSON.parse(r.value) } : r;
  }

  // compile the mu. Sharing Python, the Python (with the imports LeetCode
  // would preload: aced runs plain Python) goes into aced's editor;
  // sharing mu, only the errors show
  async function sync() {
    if (!on || swapping) return;
    const state = on;
    const model = muModel();
    const src = model.getValue();
    const r = await compiled(model);
    if (on !== state || swapping || model.isDisposed() || src !== model.getValue()) return;
    if (r.ok && on.share === "python") {
      on.origin = r.origin;
      const target = on.py.getModel();
      if (target && target.getValue() !== r.py) target.setValue(r.py);
      mark();
    }
    say(r.ok ? "mu: Cmd+Enter runs" : r.error, !r.ok);
  }

  // sharing Python: the Python lines the mu line under the cursor made
  function mark() {
    if (on?.share !== "python" || !on.origin) return;
    const at = on.editor.getPosition()?.lineNumber;
    const lines = on.origin.flatMap((mu, k) => (mu === at ? [k + 1] : []));
    on.marks.set(lines.map((n) => ({
      range: new window.monaco.Range(n, 1, n, 1),
      options: { isWholeLine: true, className: "mu-from", linesDecorationsClassName: "mu-from-edge" },
    })));
    if (lines.length) on.py.revealLinesInCenterIfOutsideViewport(lines[0], lines[lines.length - 1]);
  }

  function save() {
    if (!on || swapping) return;
    ask("set", { key: `mu:aced:${on.id}`, value: muModel().getValue() });
  }

  // Run code or Run tests. Sharing Python, the Python is in aced's editor
  // already. Sharing mu, it takes the mu's place for the moment aced reads
  // its editor, and the mu comes back.
  let passing = false; // our own click on aced's button
  async function run(button = runButton()) {
    if (!on || swapping || !button) return;
    clearTimeout(saving);
    save();
    const press = () => {
      passing = true;
      try {
        button.click();
      } finally {
        passing = false;
      }
    };
    if (on.share === "python") {
      await sync();
      if (!on) return;
      await sleep(150); // aced reads its editor through the change event
      press();
      on?.editor.focus();
      return;
    }
    const state = on;
    const model = on.py.getModel();
    const mu = model.getValue();
    const r = await compiled(model);
    if (on !== state || mu !== model.getValue()) return;
    if (!r.ok) return say(r.error, true);
    const view = on.py.saveViewState();
    swapping = true;
    try {
      model.setValue(r.py);
      await sleep(150);
      press();
      await sleep(600);
    } finally {
      if (!model.isDisposed()) model.setValue(mu);
      swapping = false;
      if (on === state) {
        on.py.restoreViewState(view);
        on.py.focus();
      }
    }
  }

  // the reason mu did not open, across the foot of aced's editor for a few seconds
  function refuse(py, text) {
    const host = py.getContainerDomNode();
    if (getComputedStyle(host).position === "static") host.style.position = "relative";
    const note = document.createElement("div");
    note.textContent = text;
    note.style.cssText = "position:absolute;left:0;right:0;bottom:0;z-index:20;padding:2px 8px;font:12px system-ui,sans-serif;background:#fdecea;color:#c0392b;";
    host.append(note);
    setTimeout(() => note.remove(), 8000);
    ask("set", { key: `mu:on:aced:${pageId()}`, value: false });
    showLabel();
  }

  // the mu to open with: what the page kept, else aced's Python as mu;
  // null (and the reason shown) when that Python does not convert
  async function muFor(py, id) {
    const kept = await ask("get", { key: `mu:aced:${id}` });
    if (kept) return kept;
    const r = await ask("starter", { src: py.getValue() });
    if (r.ok) return r.value;
    // an empty mu would compile to nothing and wipe aced's editor
    refuse(py, `mu cannot convert this starter: ${r.error}`);
    return null;
  }

  function style() {
    if (document.getElementById("mu-style")) return;
    const css = document.createElement("style");
    css.id = "mu-style";
    css.textContent = ".mu-from{background:rgba(255,196,0,.16)}.mu-from-edge{background:#f5b800;width:3px!important;margin-left:3px}";
    document.head.append(css);
  }

  // open mu in a mode. `text` is the mu when the caller has it (the other
  // mode's); `asIs` when aced's editor holds the mu already (a shared mu,
  // after a reload).
  async function enter(share, text = null, asIs = false) {
    const py = acedEditor();
    const id = pageId();
    if (!py || !id || on || entering) return;
    entering = true;
    try {
      if (text === null && !asIs) text = await muFor(py, id);
      if (text === null && !asIs) return;
      register();
      style();
      const host = py.getContainerDomNode();
      if (getComputedStyle(host).position === "static") host.style.position = "relative";
      if (share === "mu") {
        const model = py.getModel();
        if (!asIs && model.getValue() !== text) model.setValue(text);
        window.monaco.editor.setModelLanguage(model, "mu");
        const status = foot(host);
        status.style.cssText += "position:absolute;left:0;right:0;bottom:0;z-index:20;";
        host.append(status);
        const was = { tabSize: model.getOptions().tabSize, insertSpaces: model.getOptions().insertSpaces };
        model.updateOptions({ tabSize: 2, insertSpaces: true });
        const heard = model.onDidChangeContent(changed);
        on = { id, share, py, model, status, undo: () => {
          heard.dispose();
          status.remove();
          if (!model.isDisposed()) model.updateOptions(was);
        } };
      } else {
        // the mu in the left half, aced's editor (read only: the mu is the source) in the right half
        const frame = host.parentElement;
        if (getComputedStyle(frame).position === "static") frame.style.position = "relative";
        const was = { width: host.style.width, marginLeft: host.style.marginLeft, readOnly: py.getRawOptions().readOnly };
        host.style.width = "50%";
        host.style.marginLeft = "50%";
        py.updateOptions({ readOnly: true });
        const box = document.createElement("div");
        box.style.cssText = "position:absolute;left:0;top:0;bottom:0;width:50%;z-index:20;display:flex;flex-direction:column;box-sizing:border-box;border-right:1px solid rgba(128,128,128,.35);";
        const pane = document.createElement("div");
        pane.style.cssText = "flex:1;min-height:0;";
        const status = foot(host);
        box.append(pane, status);
        frame.append(box);
        const { EditorOption } = window.monaco.editor;
        const model = window.monaco.editor.createModel(text, "mu");
        const editor = window.monaco.editor.create(pane, {
          model, automaticLayout: true, fontSize: py.getOption(EditorOption.fontSize),
          fontFamily: py.getOption(EditorOption.fontFamily), lineHeight: py.getOption(EditorOption.lineHeight),
          tabSize: 2, insertSpaces: true, detectIndentation: false,
          minimap: { enabled: false }, scrollBeyondLastLine: false,
        });
        model.onDidChangeContent(changed);
        editor.onDidChangeCursorPosition(mark);
        const marks = py.createDecorationsCollection([]);
        on = { id, share, py, model, status, editor, box, origin: null, marks, undo: () => {
          marks.clear();
          editor.dispose();
          model.dispose();
          box.remove();
          host.style.width = was.width;
          host.style.marginLeft = was.marginLeft;
          py.updateOptions({ readOnly: !!was.readOnly });
        } };
        editor.focus();
      }
      ask("set", { key: `mu:on:aced:${id}`, value: share });
      if (!asIs) save();
      showLabel();
      sync();
    } finally {
      entering = false;
    }
  }

  function changed() {
    if (swapping) return;
    clearTimeout(saving);
    saving = setTimeout(() => {
      save();
      sync();
    }, 300);
  }

  // close mu. `forget`: the page opens in Python the next time. Leaving a
  // shared mu for Python puts the Python it compiles to in the editor.
  async function leave(forget = true, toPython = true) {
    if (!on) return null;
    clearTimeout(saving);
    const state = on;
    const mu = muModel().getValue();
    if (forget) ask("set", { key: `mu:on:aced:${on.id}`, value: false });
    on = null;
    state.undo();
    if (state.share === "mu") {
      const model = state.py.getModel();
      if (model && !model.isDisposed()) {
        window.monaco.editor.setModelMarkers(model, "mu", []);
        window.monaco.editor.setModelLanguage(model, "python");
        if (toPython) {
          const r = await ask("plain", { src: mu });
          if (r.ok && model.getValue() === mu) model.setValue(r.value);
        }
      }
    }
    showLabel();
    return mu;
  }

  // the menu chose a mode, or Python
  async function choose(share) {
    if (entering || swapping) return;
    if (on?.share === share) return;
    if (!share) return leave();
    // from the other mode the mu goes along; a shared mu stays in aced's editor
    const mu = on ? await leave(false, false) : null;
    await enter(share, mu);
    if (!on) showLabel();
  }

  // Cmd+Enter in the mu: aced's own shortcut would run before the last
  // compile, or run a shared mu as Python
  window.addEventListener("keydown", (e) => {
    if (!on || !(e.metaKey || e.ctrlKey) || e.key !== "Enter") return;
    const home = on.share === "python" ? on.box : on.py.getContainerDomNode();
    if (!home.contains(e.target)) return;
    e.preventDefault();
    e.stopImmediatePropagation();
    run();
  }, true);

  // sharing mu: aced's Run code and Run tests would send the mu as Python
  window.addEventListener("click", (e) => {
    if (on?.share !== "mu" || passing) return;
    const button = e.target.closest?.("button");
    if (!button || !/^Run (code|tests)/.test(button.textContent.trim())) return;
    e.preventDefault();
    e.stopImmediatePropagation();
    run(button);
  }, true);

  // the language menu: the two mu options under Python; the label and the
  // chosen option follow the mode (React sets the select back on every render)
  function addOption(select) {
    if (!select.querySelector('option[value^="mu:"]')) {
      let after = select.querySelector('option[value="python"]');
      for (const [share, text] of Object.entries(MODES)) {
        const option = document.createElement("option");
        option.value = `mu:${share}`;
        option.textContent = text;
        after.after(option);
        after = option;
      }
      select.addEventListener("change", (e) => {
        if (select.value.startsWith("mu:")) {
          e.stopImmediatePropagation(); // aced never hears of mu
          if (acedEditor()) choose(select.value.slice(3));
          else select.value = "python";
        } else {
          leave();
        }
      }, true);
    }
    if (on && select.value !== `mu:${on.share}`) select.value = `mu:${on.share}`;
  }
  function showLabel() {
    const select = langSelect();
    const label = select?.nextElementSibling;
    const text = on ? MODES[on.share] : "Python";
    if (label && label.tagName === "SPAN" && (on || /^mu/.test(label.textContent)) && label.textContent !== text) label.textContent = text;
    if (select && !on && select.value.startsWith("mu:")) select.value = "python";
  }

  // every tick: the menu, a new page, a rebuilt editor, a label React reset
  let seen = null;
  async function tick() {
    const select = langSelect();
    if (select) addOption(select);
    const id = pageId();
    // aced rebuilt its editor, or gave it a new model under a shared mu
    const gone = on && (!on.status.isConnected || !on.py.getModel() || (on.share === "mu" && on.py.getModel() !== on.model));
    if (on && !swapping && (id !== on.id || gone)) {
      leave(false, false);
      seen = null; // a rebuilt editor on the same page gets the mu back
    }
    if (on) {
      showLabel();
      // React may set aced's model back to Python
      if (on.share === "mu" && on.py.getModel()?.getLanguageId() !== "mu") window.monaco.editor.setModelLanguage(on.py.getModel(), "mu");
    }
    if (id && !on && !entering && acedEditor() && seen !== id) {
      seen = id;
      const share = await ask("get", { key: `mu:on:aced:${id}` });
      // a shared mu is in aced's editor already: aced keeps what was written
      if (share === "mu") enter("mu", null, true);
      else if (share) enter("python");
    }
    if (!id) seen = null;
  }

  const start = () => {
    new MutationObserver(() => requestAnimationFrame(tick)).observe(document.body, { childList: true, subtree: true });
    setInterval(tick, 1000);
  };
  if (document.body) start();
  else document.addEventListener("DOMContentLoaded", start);
})();
