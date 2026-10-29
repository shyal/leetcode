// The side panel: mu on top, the Python it compiles to below (compiled
// by the offscreen document through the background page). Run and
// Submit put the mu (commented) and the Python into LeetCode's editor and
// press LeetCode's own button; on an aced.io page Run puts the Python
// into aced's editor and presses Run code. The mu is kept per page in
// chrome.storage.local, under the keys the page scripts use, so each one
// opens with what was written for it.

const $ = (id) => document.getElementById(id);
const PROBLEM = /^https:\/\/leetcode\.com(?:\/contest\/[^/]+)?\/problems\/([^/?#]+)/;
const ACED = /^https:\/\/www\.aced\.io\/(practice|questions)\/([^/?#]+)/;
// the storage key's tail: the LeetCode slug, or aced:practice/<session id>, aced:questions/<number>
const pageKey = (url) => PROBLEM.exec(url)?.[1] || (ACED.test(url) ? `aced:${ACED.exec(url)[1]}/${ACED.exec(url)[2]}` : null);
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
  // aced runs plain Python with no preloads, and a peer reads it: the
  // imports it needs on top, and no quoted mu
  const aced = slug?.startsWith("aced:");
  const [py, sub] = await Promise.all([ask(aced ? "plain" : "transpile", src), aced ? null : ask("submission", src)]);
  if (src !== $("mu").value) return; // typed on meanwhile: a newer compile follows
  if (!py.ok) return status(py.error, "err");
  $("py").textContent = py.value;
  code = aced ? py.value : sub.value;
  status("");
  $("run").disabled = $("submit").disabled = !tabId;
}

async function follow() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const next = tab ? pageKey(tab.url || "") : null;
  tabId = next ? tab.id : null;
  if (next === slug) return compile();
  slug = next;
  $("slug").textContent = slug || "no problem open";
  const key = `mu:${slug}`;
  $("mu").value = slug ? (await chrome.storage.local.get(key))[key] || "" : "";
  compile();
}

// runs in the page: the Monaco editor (LeetCode's Python3, aced's Python)
// and the Run / Submit button (aced has Run code only)
function press(code, which) {
  const models = window.monaco?.editor?.getModels?.() || [];
  const model = models.find((m) => /^python3?$/.test(m.getLanguageId()));
  if (!model) {
    const langs = models.filter((m) => m.getLanguageId() !== "mu").map((m) => m.getLanguageId()).join(", ");
    return langs ? `The editor is set to ${langs}. Switch it to Python.` : "No code editor on this page.";
  }
  model.setValue(code);
  const button = document.querySelector(`[data-e2e-locator="console-${which}-button"]`) ||
    (which === "run" ? [...document.querySelectorAll("button")].find((b) => b.textContent.trim().startsWith("Run code")) : null);
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
