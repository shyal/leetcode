#!/usr/bin/env node
// lc_cookies - copy the leetcode.com login cookies out of a running browser
// that exposes the Chrome DevTools Protocol, into the file utils/rs/lc_submit
// reads. Plain CDP over node's own WebSocket, no dependencies.
//
//   LC_CDP_ENDPOINT   the browser's devtools http endpoint (required)
//   LC_COOKIE_FILE    where to write (default ~/.leetcode_cookies.json)
//
// `make lc-login` runs this.
const endpoint = process.env.LC_CDP_ENDPOINT;
if (!endpoint) {
  console.error("set LC_CDP_ENDPOINT to the browser's devtools endpoint");
  process.exit(2);
}
const out = process.env.LC_COOKIE_FILE || `${process.env.HOME}/.leetcode_cookies.json`;

const targets = await (await fetch(`${endpoint}/json`)).json();
const page = targets.find((t) => t.type === "page");
if (!page) {
  console.error("no page target at LC_CDP_ENDPOINT");
  process.exit(1);
}
const ws = new WebSocket(page.webSocketDebuggerUrl);
await new Promise((r) => (ws.onopen = r));
ws.send(JSON.stringify({ id: 1, method: "Network.getCookies", params: { urls: ["https://leetcode.com"] } }));
const reply = await new Promise((r) => (ws.onmessage = (m) => r(JSON.parse(m.data))));
ws.close();
const jar = Object.fromEntries((reply.result?.cookies ?? []).map((c) => [c.name, c.value]));
if (!jar.LEETCODE_SESSION || !jar.csrftoken) {
  console.error("no LEETCODE_SESSION cookie in that browser: log in to leetcode.com there first.");
  process.exit(1);
}
const { writeFileSync } = await import("node:fs");
writeFileSync(
  out,
  JSON.stringify({ LEETCODE_SESSION: jar.LEETCODE_SESSION, csrftoken: jar.csrftoken }, null, 2) + "\n",
  { mode: 0o600 },
);
console.log(`wrote ${out}`);
