// The toolbar button opens the mu panel beside the page. Compile requests
// ({op: "submission" | "transpile" | "starter", src}) from the panel and
// from the page go to the offscreen document, which runs Pyodide.

chrome.sidePanel.setPanelBehavior({ openPanelOnActionClick: true });

const OPS = new Set(["submission", "transpile", "starter"]);
let opening = null;

async function offscreen() {
  if (await chrome.offscreen.hasDocument()) return;
  opening ??= chrome.offscreen
    .createDocument({ url: "offscreen.html", reasons: ["WORKERS"], justification: "runs the mu compiler in Pyodide" })
    .finally(() => (opening = null));
  await opening;
}

chrome.runtime.onMessage.addListener((msg, _sender, reply) => {
  if (msg.target === "offscreen" || !OPS.has(msg.op)) return;
  offscreen()
    .then(() => chrome.runtime.sendMessage({ ...msg, target: "offscreen" }))
    .then(reply, (err) => reply({ ok: false, error: String(err) }));
  return true;
});
