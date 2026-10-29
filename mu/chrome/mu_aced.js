// mu as a language in aced.io's editor: the practice page (a live
// session with a peer) and the question pages. Runs in the page itself
// (it needs the page's `monaco`); ask, register and OPENS_BLOCK come from
// mu_common.js.
//
// Choosing mu in the language menu lays a second Monaco editor, holding
// the mu, over aced's. Each change compiles, and the Python goes into
// aced's editor at once: a peer sees Python as it is written, and Run
// code (the button, or Cmd+Enter in the mu) and Run tests run that
// Python. The mu and the choice of mu are kept per page.

(() => {
  const { ask, register } = window.__mu;
  const PAGE = /^\/(practice|questions)\/([^/?#]+)/; // a session id, or a question's number
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

  const pageId = () => {
    const m = PAGE.exec(location.pathname);
    return m ? `${m[1]}/${m[2]}` : null;
  };
  const pyEditor = () => window.monaco?.editor.getEditors().find((e) => e.getModel()?.getLanguageId() === "python");
  // aced's language menu: a native select, transparent, over a button that shows the label
  const langSelect = () =>
    [...document.querySelectorAll("select")].find((s) => [...s.options].some((o) => o.value === "python")) || null;
  const runButton = () => [...document.querySelectorAll("button")].find((b) => b.textContent.trim().startsWith("Run code"));

  let on = null; // {id, editor, model, box, status, py}
  let entering = false;
  let saving = null;

  function say(text, bad = false) {
    if (!on) return;
    on.status.textContent = text;
    on.status.style.color = bad ? "#c0392b" : "";
  }

  // compile the mu; when it compiles, the Python (with the imports LeetCode
  // would preload: aced runs plain Python) goes into aced's editor
  async function sync() {
    if (!on) return;
    const { model } = on;
    const src = model.getValue();
    const r = await ask("plain", { src });
    if (!on || on.model !== model || src !== model.getValue()) return;
    const line = r.ok ? 0 : Number(/^line (\d+)/.exec(r.error)?.[1] || 1);
    window.monaco.editor.setModelMarkers(model, "mu", r.ok ? [] : [{
      severity: window.monaco.MarkerSeverity.Error, message: r.error,
      startLineNumber: line, endLineNumber: line, startColumn: 1, endColumn: model.getLineMaxColumn(line),
    }]);
    if (r.ok) {
      on.py = r.value;
      const target = pyEditor()?.getModel();
      if (target && target.getValue() !== r.value) target.setValue(r.value);
    }
    say(r.ok ? "mu: Cmd+Enter runs" : r.error, !r.ok);
  }

  async function run() {
    if (!on) return;
    clearTimeout(saving);
    await ask("set", { key: `mu:aced:${on.id}`, value: on.model.getValue() });
    await sync();
    if (!on) return;
    await sleep(150); // aced reads its editor through the change event
    runButton()?.click();
    on?.editor.focus();
  }

  async function enter() {
    const py = pyEditor();
    const s = pageId();
    if (!py || !s || on || entering) return;
    entering = true;
    try {
      let text = await ask("get", { key: `mu:aced:${s}` });
      if (!text) {
        const r = await ask("starter", { src: py.getValue() });
        text = r.ok ? r.value : "";
      }
      register();
      const host = py.getContainerDomNode();
      if (getComputedStyle(host).position === "static") host.style.position = "relative";
      const box = document.createElement("div");
      box.style.cssText = "position:absolute;inset:0;z-index:20;display:flex;flex-direction:column;";
      const bg = getComputedStyle(host.querySelector(".monaco-editor-background") || host).backgroundColor;
      const pane = document.createElement("div");
      pane.style.cssText = "flex:1;min-height:0;";
      const status = document.createElement("div");
      status.style.cssText = `padding:2px 8px;font:12px system-ui,sans-serif;opacity:.8;background:${bg};color:#777;`;
      box.append(pane, status);
      host.append(box);
      const { EditorOption } = window.monaco.editor;
      const model = window.monaco.editor.createModel(text, "mu");
      const editor = window.monaco.editor.create(pane, {
        model, automaticLayout: true, fontSize: py.getOption(EditorOption.fontSize),
        fontFamily: py.getOption(EditorOption.fontFamily), lineHeight: py.getOption(EditorOption.lineHeight),
        tabSize: 2, insertSpaces: true, detectIndentation: false,
        minimap: { enabled: false }, scrollBeyondLastLine: false,
      });
      on = { id: s, editor, model, box, status, py: null };
      model.onDidChangeContent(() => {
        clearTimeout(saving);
        saving = setTimeout(() => {
          ask("set", { key: `mu:aced:${s}`, value: model.getValue() });
          sync();
        }, 300);
      });
      ask("set", { key: `mu:on:aced:${s}`, value: true });
      showLabel("mu");
      sync();
      editor.focus();
    } finally {
      entering = false;
    }
  }

  function leave(forget = true) {
    if (!on) return;
    if (forget) ask("set", { key: `mu:on:aced:${on.id}`, value: false });
    on.editor.dispose();
    on.model.dispose();
    on.box.remove();
    on = null;
    showLabel("Python");
  }

  // Cmd+Enter in the mu: aced's own shortcut would run before the last compile
  window.addEventListener("keydown", (e) => {
    if (!on || !(e.metaKey || e.ctrlKey) || e.key !== "Enter" || !on.box.contains(e.target)) return;
    e.preventDefault();
    e.stopImmediatePropagation();
    run();
  }, true);

  // the language menu: a mu option under Python; the label and the chosen
  // option follow the mode (React sets the select back on every render)
  function addOption(select) {
    if (!select.querySelector('option[value="mu"]')) {
      const option = document.createElement("option");
      option.value = "mu";
      option.textContent = "mu";
      select.querySelector('option[value="python"]').after(option);
      select.addEventListener("change", (e) => {
        if (select.value === "mu") {
          e.stopImmediatePropagation(); // aced never hears of mu
          if (pyEditor()) enter();
          else select.value = "python";
        } else {
          leave();
        }
      }, true);
    }
    if (on && select.value !== "mu") select.value = "mu";
  }
  function showLabel(text) {
    const select = langSelect();
    const label = select?.nextElementSibling;
    if (label && label.tagName === "SPAN" && label.textContent !== text) label.textContent = text;
    if (select && !on && select.value === "mu") select.value = "python";
  }

  // every tick: the menu, a new page, a rebuilt editor, a label React reset
  let seen = null;
  async function tick() {
    const select = langSelect();
    if (select) addOption(select);
    const s = pageId();
    if (on && (s !== on.id || !on.box.isConnected)) {
      leave(false);
      seen = null; // a rebuilt editor on the same page gets the mu back
    }
    if (on) showLabel("mu");
    if (s && !on && !entering && pyEditor() && seen !== s) {
      seen = s;
      if (await ask("get", { key: `mu:on:aced:${s}` })) enter();
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
