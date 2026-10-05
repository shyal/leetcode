// The webview: draws the columns layout.js computes, and fills the side
// panel from `kg_explore show`. A click on a vertex makes it the focus.
/* global acquireVsCodeApi, build, neighbourhood */
const vscode = acquireVsCodeApi();
const NS = "http://www.w3.org/2000/svg";
const W = 250;
const H = 26;
const GAP_X = 70;
const GAP_Y = 8;
const DEPTH = 2;
const CAP = 12;
const CAP_OPEN = 60;
const LABEL = 34;

const svg = document.getElementById("svg");
const detail = document.getElementById("detail");
const message = document.getElementById("message");
const search = document.getElementById("search");

let graph = null;
let g = null;
let focus = (vscode.getState() || {}).focus || null;
let cap = CAP;
let lastCurrent;

function s(tag, attrs, text) {
  const e = document.createElementNS(NS, tag);
  for (const [k, v] of Object.entries(attrs || {})) e.setAttribute(k, v);
  if (text !== undefined) e.textContent = text;
  return e;
}

function h(tag, attrs, ...children) {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs || {})) {
    if (k === "onclick") e.addEventListener("click", v);
    else if (k === "disabled") e.disabled = v;
    else e.setAttribute(k, v);
  }
  for (const c of children.flat()) {
    if (c !== null && c !== undefined && c !== false) e.append(c);
  }
  return e;
}

// How a vertex is coloured: a node by its status, a drill by its latest
// rep, a problem by whether it has a rep at all.
function look(v) {
  if (v.kind === "node") return v.status.toLowerCase();
  if (v.kind === "drill") {
    if (v.disabled) return "disabled";
    if (v.reps === 0) return "missing";
    return v.clean ? "solid" : "fragile";
  }
  return v.reps > 0 ? "" : "missing";
}

function about(v) {
  if (v.kind === "node") return `${v.label}: ${v.status}`;
  if (v.kind === "drill") {
    if (v.disabled) return `${v.label}: disabled`;
    if (v.reps === 0) return `${v.label}: never done`;
    return `${v.label}: ${v.reps} reps, last ${v.last}, due ${v.due}`;
  }
  return `${v.label}: ${v.reps} reps`;
}

function draw() {
  const n = neighbourhood(g, focus, DEPTH, cap);
  const tallest = Math.max(...n.columns.map((c) => c.ids.length + (c.more ? 1 : 0)));
  const height = tallest * (H + GAP_Y);
  const pos = new Map();
  n.columns.forEach((c, i) => {
    const rows = c.ids.length + (c.more ? 1 : 0);
    const top = (height - rows * (H + GAP_Y)) / 2;
    c.x = i * (W + GAP_X);
    c.top = top;
    c.ids.forEach((id, r) => pos.set(id, { x: c.x, y: top + r * (H + GAP_Y) }));
  });
  svg.replaceChildren();
  svg.setAttribute("width", n.columns.length * (W + GAP_X));
  svg.setAttribute("height", height + GAP_Y);

  for (const [u, v] of n.edges) {
    const a = pos.get(u);
    const b = pos.get(v);
    const y1 = a.y + H / 2;
    const y2 = b.y + H / 2;
    let d;
    if (a.x === b.x) {
      // both in one column: a bow on the right of the column
      const x = a.x + W;
      d = `M ${x} ${y1} C ${x + 30} ${y1}, ${x + 30} ${y2}, ${x} ${y2}`;
    } else {
      const x1 = a.x < b.x ? a.x + W : a.x;
      const x2 = a.x < b.x ? b.x : b.x + W;
      const mid = (x1 + x2) / 2;
      d = `M ${x1} ${y1} C ${mid} ${y1}, ${mid} ${y2}, ${x2} ${y2}`;
    }
    const on = u === focus || v === focus;
    svg.append(s("path", { d, class: on ? "edge focus" : "edge" }));
  }

  for (const c of n.columns) {
    for (const id of c.ids) {
      const v = g.vertices.get(id);
      const p = pos.get(id);
      const classes = ["vertex", look(v)];
      if (id === focus) classes.push("focus");
      if (id === graph.current) classes.push("current");
      const group = s("g", { class: classes.join(" "), transform: `translate(${p.x},${p.y})` });
      const rx = v.kind === "problem" ? H / 2 : v.kind === "node" ? 6 : 0;
      group.append(s("title", {}, about(v)));
      group.append(s("rect", { width: W, height: H, rx }));
      const label = v.label.length > LABEL ? `${v.label.slice(0, LABEL - 1)}...` : v.label;
      group.append(s("text", { x: 10, y: H / 2 }, label));
      if (v.kind === "drill" && !v.disabled && v.due && v.due <= graph.today) {
        group.append(s("circle", { class: "due", cx: W - 12, cy: H / 2, r: 4 }));
      }
      group.addEventListener("click", () => focusOn(id));
      svg.append(group);
    }
    if (c.more) {
      const y = c.top + c.ids.length * (H + GAP_Y);
      const more = s("g", { class: "more", transform: `translate(${c.x},${y})` });
      more.append(s("text", { x: 10, y: H / 2 }, `${c.more} more`));
      more.addEventListener("click", () => {
        cap = CAP_OPEN;
        draw();
      });
      svg.append(more);
    }
  }
}

function focusOn(id) {
  if (!g.vertices.has(id)) return;
  focus = id;
  cap = CAP;
  vscode.setState({ focus });
  message.textContent = "";
  draw();
  vscode.postMessage({ type: "show", id });
}

function ref(id) {
  const v = g.vertices.get(id);
  if (!v) return document.createTextNode(id);
  return h("a", { class: "ref", onclick: () => focusOn(id) }, v.kind === "node" ? id : v.label);
}

// "a, b and c" over clickable ids.
function refs(ids) {
  const out = [];
  ids.forEach((id, i) => {
    if (i > 0) out.push(i === ids.length - 1 ? " and " : ", ");
    out.push(ref(id));
  });
  return out;
}

function repsTable(reps) {
  if (!reps.length) return h("p", {}, "No reps yet.");
  const rows = [h("tr", {}, ["#", "Date", "Minutes", "Help", "Result"].map((t) => h("th", {}, t)))];
  reps.forEach((r, i) => {
    rows.push(
      h(
        "tr",
        { class: "rep", title: r.file, onclick: () => vscode.postMessage({ type: "open", path: r.file }) },
        h("td", {}, String(i + 1)),
        h("td", {}, r.date),
        h("td", {}, r.minutes === null ? "" : String(r.minutes)),
        h("td", {}, r.assist),
        h("td", {}, r.verdict)
      )
    );
    if (r.note) rows.push(h("tr", { class: "note" }, h("td", {}), h("td", { colspan: "4" }, r.note)));
  });
  return h("table", {}, rows);
}

function drillPanel(d) {
  const refused = !d.disabled && d.refused_by.length > 0;
  const open = (path) => () => vscode.postMessage({ type: "open", path });
  return [
    h("h2", {}, `${d.id} ${d.title}`),
    h("p", {}, "Trains ", refs(d.trains), "."),
    d.after.length ? h("p", {}, "Comes after ", refs(d.after), ".") : null,
    h(
      "p",
      {},
      d.disabled
        ? `Disabled. The picker does not serve it; make drill ${d.id} still does.`
        : d.due
          ? `Due ${d.due}.`
          : "Never done."
    ),
    h(
      "div",
      { class: "buttons" },
      h("button", { onclick: open(d.file) }, "Open drill"),
      d.reference ? h("button", { class: "quiet", onclick: open(d.reference) }, "Reference solution") : null,
      h(
        "button",
        {
          class: "quiet",
          disabled: refused,
          onclick: () => vscode.postMessage({ type: "flag", id: d.id, on: !d.disabled }),
        },
        d.disabled ? "Enable" : "Disable"
      )
    ),
    refused
      ? h(
          "p",
          {},
          d.refused_by.map((p) => `${p.id}. ${p.title}`).join(", "),
          " waits on this drill, and its reps have not cleared the gate yet. It cannot be disabled before then."
        )
      : null,
    repsTable(d.reps),
  ];
}

function problemPanel(p) {
  const name = `${p.id}. ${p.title}`;
  const cache = (field) => () => vscode.postMessage({ type: "cache", id: p.id, field, title: name });
  return [
    h("h2", {}, name),
    p.moves.length ? h("p", {}, "Uses ", refs(p.moves), ".") : null,
    p.after.length ? h("p", {}, "Comes after ", refs(p.after), ".") : null,
    p.held_behind ? h("p", {}, "Held behind ", ref(p.held_behind), ".") : null,
    p.due ? h("p", {}, `Review due ${p.due}.`) : null,
    p.cache
      ? h(
          "div",
          { class: "buttons" },
          h("button", { onclick: cache("code") }, "Statement and stub"),
          h("button", { class: "quiet", onclick: cache("solution") }, "Reference solution")
        )
      : h("p", {}, "This problem is not in the cache."),
    repsTable(p.reps),
  ];
}

function nodePanel(n) {
  const last = n.last ? ` Last rep ${n.last}.` : "";
  return [
    h("h2", {}, n.name),
    h("p", {}, n.id),
    n.desc ? h("p", {}, n.desc) : null,
    h("p", {}, `${n.status}. Ownership ${n.degree} over ${n.carriers} problems.${last}`),
    n.prereqs.length ? h("p", {}, "Comes after ", refs(n.prereqs), ".") : null,
    n.drills.length ? h("p", {}, "Drills: ", refs(n.drills), ".") : h("p", {}, "No drills."),
  ];
}

function showDetail(d) {
  const parts = d.kind === "drill" ? drillPanel(d) : d.kind === "problem" ? problemPanel(d) : nodePanel(d);
  detail.replaceChildren(...parts.filter(Boolean));
}

function find(text) {
  const q = text.trim().toLowerCase();
  if (!q) return null;
  if (g.vertices.has(q)) return q;
  for (const v of g.vertices.values()) {
    if (v.label.toLowerCase().includes(q)) return v.id;
  }
  return null;
}

search.addEventListener("keydown", (e) => {
  if (e.key !== "Enter" || !g) return;
  const id = find(search.value);
  if (id) focusOn(id);
  else message.textContent = `Nothing matches "${search.value}".`;
});

document.getElementById("current").addEventListener("click", () => {
  if (!graph) return;
  if (graph.current) focusOn(graph.current);
  else message.textContent = "current.py holds no problem or drill.";
});

window.addEventListener("message", ({ data: m }) => {
  if (m.type === "error") message.textContent = m.text;
  if (m.type === "detail" && m.data.id === focus) showDetail(m.data);
  if (m.type === "graph") {
    graph = m.data;
    g = build(graph);
    // a new problem or drill in current.py takes the focus
    const moved = graph.current && graph.current !== lastCurrent;
    lastCurrent = graph.current;
    if (moved || !focus || !g.vertices.has(focus)) {
      focus = graph.current || focus || graph.nodes[0].id;
      if (!g.vertices.has(focus)) focus = graph.nodes[0].id;
    }
    focusOn(focus);
  }
});

vscode.postMessage({ type: "ready" });
