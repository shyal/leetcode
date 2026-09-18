#!/usr/bin/env node
// lc_fetch - one HTTP request to leetcode.com, made from inside a running
// browser that exposes the Chrome DevTools Protocol. The request runs as a
// fetch() in a leetcode.com tab, so it carries the browser's login, its TLS
// fingerprint and its Cloudflare clearance. Cloudflare's WAF in front of
// leetcode rejects some code bodies as SQL injection ("(a or b) or (c or d)"
// did it on 2026-09-17) from anything that is not a real browser, copied
// cookies included; this is the only transport that submits every solution.
// Plain CDP over node's own WebSocket, no dependencies.
//
//   node misc/lc_fetch.mjs METHOD PATH [< body]    # PATH is under https://leetcode.com
//
// Prints the status code on the first line, the response body after it.
// A body on stdin is sent as application/json with the csrf header set.
//
//   LC_CDP_ENDPOINT   the browser's devtools http endpoint (required)
//
// utils/rs/lc_submit runs this.
const endpoint = process.env.LC_CDP_ENDPOINT;
if (!endpoint) {
  console.error("set LC_CDP_ENDPOINT to the browser's devtools endpoint");
  process.exit(2);
}
const [method, path] = process.argv.slice(2);
if (!method || !path) {
  console.error("usage: lc_fetch.mjs METHOD PATH [< body]");
  process.exit(2);
}
let body = "";
if (!process.stdin.isTTY) for await (const chunk of process.stdin) body += chunk;

const targets = await (await fetch(`${endpoint}/json`)).json();
let page = targets.find((t) => t.type === "page" && t.url.startsWith("https://leetcode.com/"));
// No leetcode tab: open one for the request and close it after.
const opened = page ? null : await (await fetch(`${endpoint}/json/new?https://leetcode.com/`, { method: "PUT" })).json();
page ??= opened;
const ws = new WebSocket(page.webSocketDebuggerUrl);
await new Promise((r) => (ws.onopen = r));
let nextId = 1;
// A reply never comes for an evaluate sent while the page navigates, so
// every call gives up after a while.
const evaluate = (expression, timeoutMs = 5000) =>
  new Promise((resolve) => {
    const id = nextId++;
    const timer = setTimeout(() => {
      ws.removeEventListener("message", onMessage);
      resolve({ error: `no reply from the browser in ${timeoutMs}ms` });
    }, timeoutMs);
    const onMessage = (m) => {
      const reply = JSON.parse(m.data);
      if (reply.id !== id) return;
      clearTimeout(timer);
      ws.removeEventListener("message", onMessage);
      const details = reply.result?.exceptionDetails;
      if (details) resolve({ error: details.exception?.description ?? details.text });
      else resolve(reply.result?.result?.value ?? reply);
    };
    ws.addEventListener("message", onMessage);
    ws.send(JSON.stringify({ id, method: "Runtime.evaluate", params: { expression, awaitPromise: true, returnByValue: true } }));
  });

// A freshly opened tab has no cookies until the page has loaded, and
// Cloudflare may first serve a challenge page (/?__cf_chl_rt_tk=...) that
// redirects a moment later; a fetch started during that redirect is aborted.
const settled = `document.readyState === "complete"
  && !location.href.includes("__cf_chl")
  && document.cookie.includes("csrftoken=")`;
let ready = false;
for (let i = 0; i < 30 && !(ready = (await evaluate(settled, 1000)) === true); i++) {
  await new Promise((r) => setTimeout(r, 200));
}
if (!ready) {
  ws.close();
  console.error("lc_fetch: the leetcode tab is stuck on a Cloudflare challenge; open it in the browser and let it pass");
  process.exit(1);
}
const request = {
  method,
  headers: body ? { "Content-Type": "application/json", "x-csrftoken": "CSRF" } : {},
  ...(body ? { body } : {}),
};
const expr = `(async () => {
  const req = ${JSON.stringify(request)};
  if (req.headers["x-csrftoken"]) req.headers["x-csrftoken"] = (document.cookie.match(/csrftoken=([^;]+)/) ?? [])[1] ?? "";
  const r = await fetch(${JSON.stringify(path)}, req);
  return [r.status, await r.text()];
})()`;
const result = await evaluate(expr, 30000);
ws.close();
if (opened) await fetch(`${endpoint}/json/close/${opened.id}`);
if (!Array.isArray(result)) {
  console.error(`lc_fetch: ${JSON.stringify(result)}`);
  process.exit(1);
}
const [status, text] = result;
process.stdout.write(`${status}\n${text}`);
