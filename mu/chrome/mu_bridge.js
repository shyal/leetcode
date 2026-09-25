// Between mu_page.js, which runs in LeetCode's own page, and the
// extension: the page has no chrome.* APIs, so its requests come here as
// window messages. get / set read and write chrome.storage.local (the
// panel keeps the mu under the same keys); every other op is a compile.

window.addEventListener("message", async (e) => {
  if (e.source !== window || e.data?.muReq === undefined) return;
  const { muReq, op, key, value, src } = e.data;
  let result;
  if (op === "get") result = (await chrome.storage.local.get(key))[key];
  else if (op === "set") result = await chrome.storage.local.set({ [key]: value });
  else result = await chrome.runtime.sendMessage({ op, src });
  window.postMessage({ muRes: muReq, result }, "*");
});
