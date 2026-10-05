// node --test misc/vscode-graph/layout.test.js
const test = require("node:test");
const assert = require("node:assert/strict");
const { build, neighbourhood } = require("./media/layout");

const graph = {
  nodes: [
    { id: "counter-build", name: "Build a counter", prereqs: [] },
    { id: "buckets", name: "Bucket by bounded value", prereqs: ["counter-build"] },
  ],
  drills: [
    { id: "d10", title: "Sort Bounded Values", trains: ["buckets"], after: [] },
    { id: "d11", title: "Count Smaller Values", trains: ["buckets"], after: ["d10"] },
    { id: "d12", title: "Kth Smallest Bounded Value", trains: ["buckets"], after: ["d11"] },
  ],
  problems: [
    { id: "75", title: "Sort Colors", moves: ["buckets"], after: ["d12"], reps: 0 },
    { id: "274", title: "H-Index", moves: ["buckets"], after: [], reps: 2 },
  ],
};

const cols = (n) => Object.fromEntries(n.columns.map((c) => [c.col, c.ids]));

test("a drill sits between what it comes after and what comes after it", () => {
  const n = neighbourhood(build(graph), "d11", 2, 12);
  assert.deepEqual(cols(n), {
    "-2": ["counter-build"],
    "-1": ["buckets", "d10"],
    0: ["d11"],
    1: ["d12"],
    2: ["75"],
  });
});

test("a vertex is placed once, in the column nearest the focus", () => {
  const n = neighbourhood(build(graph), "buckets", 2, 12);
  // d11 and d12 come after d10, and they also train the node directly
  assert.deepEqual(cols(n), {
    "-1": ["counter-build"],
    0: ["buckets"],
    1: ["d10", "d11", "d12", "274", "75"],
  });
  assert.ok(n.edges.some(([u, v]) => u === "d10" && v === "d11"));
});

test("a long column is cut and says how many were left out", () => {
  const n = neighbourhood(build(graph), "buckets", 1, 2);
  const right = n.columns.find((c) => c.col === 1);
  assert.deepEqual(right.ids, ["d10", "d11"]);
  assert.equal(right.more, 3);
});

test("an edge to an id the graph does not carry is dropped", () => {
  const g = build({ ...graph, problems: [{ id: "1", title: "Two Sum", moves: ["gone"], after: ["d99"], reps: 0 }] });
  assert.deepEqual(g.preds.get("1"), []);
});
