# dsa/

A scratchpad of DSA classes and reference implementations, kept as a memory aid.

Nothing here is wired into the tooling and nothing depends on it. Files are
written once, when a technique clicks, so that the shape of it (the class, the
loop, the invariant) is on disk in my own words. When a technique slips, i come
back here before looking anything up.

Things here should eventually move to `drills/`. The path, when a mental
model won't stick, is `dsa/` -> drill -> memory: first i lean on the class as
written here, then a drill makes me write it myself, then it lives in my head
and the file is just a backup. Monotonic stack went exactly that way: i started
by importing `monotonic_stack.py`, then switched to writing the stack by hand.

Some files are pointed at by `refs` in `graph/nodes.json` (see `utils/kg/kg_mirror`),
which is how a node can say "the reference implementation lives here". Most
files are not referenced by anything, and that is fine: unreferenced is not dead.

- `monotonic_stack.py`, `monotonic_stack_problems/` - the stack, its problems, and a manim scene
- `recursive_descent.py` - parser skeleton
- `sliding_window.py`, `prims_algorithm.py` - the loops, as i remember them
- `sql.py` - query idioms
- `base_conversion.py`, `ceil_div/`, `union_find/` - small scratch solves kept for the idiom
- `viz.py` - tour of the drawing helpers the harness injects (`make viz`)
