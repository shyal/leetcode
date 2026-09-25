// The side panel: mu on top, the Python it compiles to below (compiled
// by the offscreen document through the background page). Run and
// Submit put the mu (commented) and the Python into LeetCode's editor and
// press LeetCode's own button. The mu is kept per problem in
// chrome.storage.local, so each problem opens with what was written for it.

const $ = (id) => document.getElementById(id);
const PROBLEM = /^https:\/\/leetcode\.com\/problems\/([^/?#]+)/;
let slug = null;
let tabId = null;
let code = null; // the submission for the current mu, or null when it does not compile

function status(text, kind = "") {
  $("status").textContent = text;
  $("status").className = kind;
}

const ask = (op, src) => chrome.runtime.sendMessage({ op, src });

async function compile() {
  code = null;
  const src = $("mu").value;
  $("run").disabled = $("submit").disabled = true;
  if (!src.trim()) {
    $("py").textContent = "";
    return;
  }
  const [py, sub] = await Promise.all([ask("transpile", src), ask("submission", src)]);
  if (src !== $("mu").value) return; // typed on meanwhile: a newer compile follows
  if (!py.ok) return status(py.error, "err");
  $("py").textContent = py.value;
  code = sub.value;
  status("");
  $("run").disabled = $("submit").disabled = !tabId;
}

async function follow() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const m = tab && PROBLEM.exec(tab.url || "");
  const next = m ? m[1] : null;
  tabId = m ? tab.id : null;
  if (next === slug) return compile();
  slug = next;
  $("slug").textContent = slug || "no problem open";
  const key = `mu:${slug}`;
  $("mu").value = slug ? (await chrome.storage.local.get(key))[key] || "" : "";
  compile();
}

// runs in the page: LeetCode's Monaco editor and its Run / Submit buttons
function press(code, which) {
  const models = window.monaco?.editor?.getModels?.() || [];
  const model = models.find((m) => m.getLanguageId() === "python3");
  if (!model) {
    const langs = models.map((m) => m.getLanguageId()).join(", ");
    return langs ? `The editor is set to ${langs}. Switch it to Python3.` : "No code editor on this page.";
  }
  model.setValue(code);
  const button = document.querySelector(`[data-e2e-locator="console-${which}-button"]`);
  if (!button) return `No ${which} button on this page.`;
  button.click();
  return "";
}

async function send(which) {
  if (!code || !tabId) return;
  const [{ result }] = await chrome.scripting.executeScript({
    target: { tabId },
    world: "MAIN",
    func: press,
    args: [code, which],
  });
  status(result || (which === "submit" ? "Submitted." : "Running."), result ? "err" : "ok");
}

let saving = null;
$("mu").addEventListener("input", () => {
  compile();
  clearTimeout(saving);
  if (slug) saving = setTimeout(() => chrome.storage.local.set({ [`mu:${slug}`]: $("mu").value }), 300);
});

$("mu").addEventListener("keydown", (e) => {
  if (e.key === "Tab" && !e.shiftKey) {
    e.preventDefault();
    document.execCommand("insertText", false, "  "); // keeps undo working
  } else if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) {
    e.preventDefault();
    send(e.shiftKey ? "submit" : "run");
  }
});
$("run").onclick = () => send("run");
$("submit").onclick = () => send("submit");

chrome.tabs.onActivated.addListener(follow);
chrome.tabs.onUpdated.addListener((id, info) => info.url && follow());

follow();
