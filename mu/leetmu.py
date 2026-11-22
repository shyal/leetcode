"""The leet profile of mu: pydsa as the library a mu file may call, the
names sitecustomize preloads as the environment the ide completes.

`[tool.mu] profile` in pyproject.toml names this file, so `python -m mulang`,
the REPL and the ide load it for a run from the repo root; the scripts in
mu/ import it before mulang."""

import ast
import builtins
import importlib
import inspect
import os
import re
import sys
from pathlib import Path

import mulang
import pydsa

ROOT = Path(__file__).resolve().parent.parent
HARNESS = ROOT / "utils" / "harness"

# what sitecustomize puts into builtins: the builders, the drawers, the
# asserts, and the classes LeetCode defines. The stdlib names it also injects
# are not ours.
INJECTED = re.findall(
    r"^builtins\.(\w+)\s*=", (HARNESS / "sitecustomize.py").read_text(), re.M
)


def public_defs(module):
    """The public defs and classes a pydsa module defines itself."""
    tree = ast.parse(inspect.getsource(module))
    return [
        node.name
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.ClassDef))
        and not node.name.startswith("_")
    ]


# the preloaded names a submission still needs pasted: LeetCode does not
# define them
PASTED = {
    "as_list", "cells", "nbrs", "table", "like", "shape", "put", "row", "col",
    "set_row", "set_col", "in_bounds", "is_edge", "edges", "grid_bfs", "pairs",
    "triples", "substrings", "to_digits", "to_int", "num_digits", "even", "odd",
    "ceil_div", "factorial", "prime", "primes", "first_true", "last_true",
    "first_false", "last_false", "min_chunks", "Multiset", "levels", "adjacency",
    "indegrees", "components", "graph", "dijkstra", "heap",
}  # fmt: skip

# the helpers a mu file may call by name, the leet profile's library: every
# public def and class of every pydsa module that sitecustomize does not
# preload, and the PASTED names it does. A new helper in pydsa is in the
# library, with its ide hints and its paste into a submission, with nothing
# added here.
for path in sorted(Path(pydsa.__file__).parent.glob("[!_]*.mu")):
    module = importlib.import_module(f"pydsa.{path.stem}")
    mulang.library(
        module,
        *[n for n in public_defs(module) if n not in INJECTED or n in PASTED],
    )

# os is not preloaded on LeetCode. A solve that calls commonprefix gets this
# line pasted, and `import os` at the top of the file.
commonprefix = os.path.commonprefix
mulang.library(sys.modules[__name__], "commonprefix")

# the modulus of the problems that say "return it modulo 10^9 + 7". A solve
# that uses MOD gets this line pasted.
MOD = 10**9 + 7
mulang.library(sys.modules[__name__], "MOD")


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
