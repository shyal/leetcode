// mu as a language in LeetCode's editor. Runs in the page itself (it
// needs the page's `monaco`), and reaches the extension through
// mu_bridge.js.
//
// Choosing mu in the language menu sets LeetCode to Python3 and lays a
// second Monaco editor, holding the mu, over LeetCode's. LeetCode's own
// editor keeps its Python untouched while you type. Run and Submit (the
// buttons, Cmd+' and Cmd+Enter) are caught first: the mu compiles, the
// submission (the mu quoted as comments, then the Python) goes into
// LeetCode's editor, and the click goes through. The mu and the choice of
// mu are kept per problem.

(() => {
  const PROBLEM = /^\/problems\/([^/?#]+)/;
  const BUTTON = '[data-e2e-locator="console-run-button"],[data-e2e-locator="console-submit-button"]';
  const ROW = "div.group.cursor-pointer";
  const OPENS_BLOCK = /^\s*(def|memo|for|if|elif|else|while)\b|\b(sum|max|min|count)\s+(for|from)\b/;

  let seq = 0;
  const pending = new Map();
  window.addEventListener("message", (e) => {
    if (e.source !== window || e.data?.muRes === undefined) return;
    pending.get(e.data.muRes)?.(e.data.result);
    pending.delete(e.data.muRes);
  });
  const ask = (op, args = {}) =>
    new Promise((resolve) => {
      const id = ++seq;
      pending.set(id, resolve);
      window.postMessage({ muReq: id, op, ...args }, "*");
    });

  const slug = () => PROBLEM.exec(location.pathname)?.[1] || null;
  const pyEditor = () => window.monaco?.editor.getEditors().find((e) => e.getModel()?.getLanguageId() === "python3");
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  const label = (row) => row.textContent.trim();

  let on = null; // {slug, editor, model, box, status}
  let entering = false;
  let passing = false; // our own click on Run / Submit, let through

  function register() {
    const { languages } = window.monaco;
    if (languages.getLanguages().some((l) => l.id === "mu")) return;
    languages.register({ id: "mu" });
    languages.setMonarchTokensProvider("mu", {
      keywords: ["def", "memo", "for", "in", "if", "elif", "else", "while", "return", "break", "continue",
        "pass", "del", "assert", "from", "first", "import", "extends", "and", "or", "not", "is",
        "true", "false", "none", "inf"],
      builtins: ["len", "max", "min", "sum", "count", "abs", "sort", "scan", "counter", "ceil", "floor",
        "cells", "nbrs", "components", "graph", "dijkstra"],
      types: ["int", "str", "char", "bool", "float"],
      tokenizer: {
        root: [
          [/#.*$/, "comment"],
          [/[fFrRbB]{0,2}"""/, "string", "@double"],
          [/[fFrRbB]{0,2}'''/, "string", "@single"],
          [/[fFrRbB]{0,2}"[^"\n]*"/, "string"],
          [/[fFrRbB]{0,2}'[^'\n]*'/, "string"],
          [/\d+(\.\d+)?/, "number"],
          [/[A-Za-z_]\w*/, { cases: { "@keywords": "keyword", "@builtins": "predefined", "@types": "type", "@default": "identifier" } }],
          [/\.\.<|\.\.|->|<-/, "keyword"],
        ],
        double: [[/"""/, "string", "@pop"], [/./, "string"]],
        single: [[/'''/, "string", "@pop"], [/./, "string"]],
      },
    });
    languages.setLanguageConfiguration("mu", {
      comments: { lineComment: "#" },
      brackets: [["(", ")"], ["[", "]"], ["{", "}"]],
      autoClosingPairs: [
        { open: "(", close: ")" }, { open: "[", close: "]" }, { open: "{", close: "}" },
        { open: '"', close: '"' }, { open: "'", close: "'" },
      ],
      onEnterRules: [{ beforeText: OPENS_BLOCK, action: { indentAction: languages.IndentAction.Indent } }],
    });
  }

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

  async function enter() {
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
    on.editor.dispose();
    on.model.dispose();
    on.box.remove();
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
    const r = await ask("submission", { src: on.model.getValue() });
    if (!r.ok) return say(r.error, true);
    pyEditor()?.getModel().setValue(r.value);
    await sleep(150); // LeetCode reads the editor through its change events
    passing = true;
    try {
      button.click();
    } finally {
      passing = false;
    }
    on?.editor.focus();
  }, true);

  // LeetCode's own shortcuts would send the Python under the mu
  window.addEventListener("keydown", (e) => {
    if (!on || !(e.metaKey || e.ctrlKey)) return;
    const which = e.key === "Enter" ? "submit" : e.key === "'" ? "run" : null;
    if (!which) return;
    e.preventDefault();
    e.stopImmediatePropagation();
    press(which);
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
      if (pyEditor()) {
        document.dispatchEvent(new KeyboardEvent("keydown", { key: "Escape", bubbles: true }));
      } else {
        py3.click(); // LeetCode switches to Python3 and closes the menu
        for (let i = 0; i < 30 && !pyEditor(); i++) await sleep(100);
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
    if (on && (s !== on.slug || !on.box.isConnected)) {
      leave(false);
      seen = null; // a rebuilt editor on the same problem gets the mu back
    }
    if (on) showLabel("mu");
    if (s && !on && !entering && pyEditor() && seen !== s) {
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
