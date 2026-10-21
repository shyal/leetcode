"""The leet profile of mu: pydsa as the library a mu file may call, the
names sitecustomize preloads as the environment the ide completes.

`[tool.mu] profile` in pyproject.toml names this file, so `python -m mulang`,
the REPL and the ide load it for a run from the repo root; the scripts in
mu/ import it before mulang."""

import builtins
import inspect
import os
import re
from pathlib import Path

import mulang
import pydsa
from pydsa import adj, arith, combo, counting, digits, generators, grid, heaps, search

ROOT = Path(__file__).resolve().parent.parent
HARNESS = ROOT / "utils" / "harness"

# the helpers a mu file may call by name, the leet profile's library
LIBRARY = {
    generators: ["as_list"],
    grid: [
        "cells", "nbrs", "table", "like", "shape", "put", "row", "col", "set_row",
        "set_col", "in_bounds", "is_edge", "edges", "grid_bfs",
    ],
    combo: ["pairs", "triples"],
    digits: ["to_digits", "to_int", "num_digits", "even", "odd"],
    arith: ["ceil_div", "factorial"],
    search: ["first_true", "last_true", "first_false", "last_false", "min_chunks"],
    counting: ["Multiset"],
    adj: ["levels", "adjacency", "indegrees", "components", "graph", "dijkstra"],
    heaps: ["heap"],
}  # fmt: skip

for module, names in LIBRARY.items():
    mulang.library(module, *names)


def ours(obj):
    """True if obj is defined in pydsa or utils/harness, or in sitecustomize."""
    if getattr(obj, "__module__", None) == "sitecustomize":
        return True
    try:
        path = inspect.getsourcefile(obj)
    except TypeError:
        return False
    return path is not None and path.startswith(
        (os.path.dirname(pydsa.__file__), str(HARNESS))
    )


# what sitecustomize puts into builtins and we define: the builders, the
# drawers, the asserts. The stdlib names it also injects are not ours.
INJECTED = re.findall(
    r"^builtins\.(\w+)\s*=", (HARNESS / "sitecustomize.py").read_text(), re.M
)
mulang.environment(
    {
        name: getattr(builtins, name)
        for name in INJECTED
        if hasattr(builtins, name) and ours(getattr(builtins, name))
    }
)
mulang.PATHS += [str(ROOT / "utils"), str(HARNESS)]
mulang.document(ROOT / "mu" / "HELPERS.md")
# `from pydsa.digits import even` in a mu file reads pydsa/digits.mu, for
# the modules pydsa writes in mu
mulang.mu_path(Path(pydsa.__file__).resolve().parent.parent)
