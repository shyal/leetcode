// The picture the explorer draws: the focus vertex in the middle column,
// what it comes after in the columns to its left, what comes after it in
// the columns to its right, two edges out each way. Pure functions over the
// JSON kg_explore prints, so node can test them (layout.test.js) and the
// webview can load the same file.

// An edge u -> v means u comes before v: a prerequisite before its node, an
// "after" id before the drill or problem that names it, a node before the
// drills that train it and the problems that use it.
function build(graph) {
  const vertices = new Map();
  const preds = new Map();
  const succs = new Map();
  const add = (v) => {
    vertices.set(v.id, v);
    preds.set(v.id, []);
    succs.set(v.id, []);
  };
  for (const n of graph.nodes) add({ ...n, kind: "node", label: n.name });
  for (const d of graph.drills) add({ ...d, kind: "drill", label: `${d.id} ${d.title}` });
  for (const p of graph.problems) add({ ...p, kind: "problem", label: `${p.id}. ${p.title}` });
  const edge = (u, v) => {
    if (!vertices.has(u) || !vertices.has(v) || succs.get(u).includes(v)) return;
    succs.get(u).push(v);
    preds.get(v).push(u);
  };
  for (const n of graph.nodes) for (const p of n.prereqs) edge(p, n.id);
  for (const d of graph.drills) {
    for (const a of d.after) edge(a, d.id);
    for (const t of d.trains) edge(t, d.id);
  }
  for (const p of graph.problems) {
    for (const a of p.after) edge(a, p.id);
    for (const m of p.moves) edge(m, p.id);
  }
  return { vertices, preds, succs };
}

const KIND_ORDER = { node: 0, drill: 1, problem: 2 };

// Nodes, then drills, then problems; among problems the ones with reps
// first. Ids break ties by number, so d9 sorts before d10.
function order(g, ids) {
  const num = (id) => parseInt(id.replace(/^d/, ""), 10);
  return [...ids].sort((a, b) => {
    const x = g.vertices.get(a);
    const y = g.vertices.get(b);
    if (x.kind !== y.kind) return KIND_ORDER[x.kind] - KIND_ORDER[y.kind];
    if (x.kind === "problem" && (y.reps > 0) !== (x.reps > 0)) return (y.reps > 0) - (x.reps > 0);
    if (x.kind === "node") return a < b ? -1 : a > b ? 1 : 0;
    return num(a) - num(b);
  });
}

// Columns -depth..depth around the focus. A vertex is placed once, in the
// column nearest the focus. A column longer than `cap` is cut, and `more`
// carries how many were left out.
function neighbourhood(g, focus, depth, cap) {
  const placed = new Set([focus]);
  const columns = [{ col: 0, ids: [focus], more: 0 }];
  for (const [sign, next] of [[-1, g.preds], [1, g.succs]]) {
    let frontier = [focus];
    for (let k = 1; k <= depth; k++) {
      const found = [];
      for (const id of frontier) {
        for (const n of next.get(id)) {
          if (!placed.has(n) && !found.includes(n)) found.push(n);
        }
      }
      const sorted = order(g, found);
      const kept = sorted.slice(0, cap);
      for (const id of kept) placed.add(id);
      if (kept.length) columns.push({ col: sign * k, ids: kept, more: sorted.length - kept.length });
      frontier = kept;
    }
  }
  columns.sort((a, b) => a.col - b.col);
  const edges = [];
  for (const u of placed) {
    for (const v of g.succs.get(u)) if (placed.has(v)) edges.push([u, v]);
  }
  return { columns, edges };
}

if (typeof module !== "undefined") module.exports = { build, order, neighbourhood };
