// The one Pyodide the extension runs. The background page opens this
// offscreen document on the first compile; the panel and the mu mode in
// LeetCode's editor both reach it through the background page.

const CALLS = { submission: "submit.submission", transpile: "mu.transpile", starter: "submit.starter" };

const ready = (async () => {
  const py = await loadPyodide({ indexURL: chrome.runtime.getURL("pyodide/") });
  for (const f of ["mu.py", "session.py", "submit.py"]) {
    py.FS.writeFile(`/home/pyodide/${f}`, await (await fetch(f)).text());
  }
  py.runPython('import sys; sys.path.insert(0, "/home/pyodide"); import mu, submit');
  return py;
})();

chrome.runtime.onMessage.addListener((msg, _sender, reply) => {
  if (msg.target !== "offscreen") return;
  ready.then((py) => {
    py.globals.set("src", msg.src);
    try {
      reply({ ok: true, value: py.runPython(`${CALLS[msg.op]}(src)`) });
    } catch (err) {
      const last = String(err.message || err).trim().split("\n").pop();
      reply({ ok: false, error: last.replace(/^[\w.]*Error: /, "") });
    }
  }, (err) => reply({ ok: false, error: `Python did not load: ${err}` }));
  return true;
});
