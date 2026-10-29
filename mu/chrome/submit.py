"""The Python side of the extension, run in Pyodide.

submission(src): what goes in LeetCode's editor, `# mu <version>`, the mu
solution quoted as comments, then the Python it compiles to. lc_submit sends a filed
solve in the same shape.

plain(src): what goes in aced.io's editor, the Python alone, with the
imports LeetCode preloads (utils/harness/sitecustomize.py mirrors them)
for the names the Python uses: aced runs plain Python.

starter(py): the mu to start from, LeetCode's Python3 starter code
through mu/session.py stub. The starter leaves each def's body empty,
which does not parse, so every empty def first gets a `pass`."""

import ast
import re

from mulang import VERSION, transpile
from session import stub

DEF = re.compile(r"^(\s*)def .*:\s*$")

# name -> the module LeetCode preloads it from; a module's own name -> ""
PRELOADS = {
    **{n: "collections" for n in ["Counter", "OrderedDict", "defaultdict", "deque"]},
    **{n: "heapq" for n in ["heapify", "heappop", "heappush", "heappushpop", "heapreplace", "nlargest", "nsmallest"]},
    **{n: "bisect" for n in ["bisect_left", "bisect_right", "insort", "insort_left", "insort_right"]},
    **{n: "functools" for n in ["cache", "cached_property", "cmp_to_key", "lru_cache", "partial", "reduce", "wraps"]},
    **{n: "itertools" for n in ["accumulate", "chain", "combinations", "combinations_with_replacement", "cycle",
        "dropwhile", "groupby", "islice", "pairwise", "permutations", "product", "repeat", "starmap",
        "takewhile", "zip_longest"]},
    **{n: "math" for n in ["ceil", "comb", "factorial", "floor", "gcd", "inf", "isclose", "isqrt", "lcm", "log",
        "log2", "log10", "perm", "prod", "sqrt"]},
    **{n: "random" for n in ["choice", "choices", "getrandbits", "randint", "randrange", "sample", "shuffle", "uniform"]},
    **{n: "string" for n in ["ascii_letters", "ascii_lowercase", "ascii_uppercase", "digits", "hexdigits"]},
    **{n: "typing" for n in ["Any", "Callable", "Dict", "Generic", "Iterable", "Iterator", "List", "Optional",
        "Set", "Tuple", "TypeVar", "Union"]},
    "maxsize": "sys",
    "SortedList": "sortedcontainers", "SortedDict": "sortedcontainers", "SortedSet": "sortedcontainers",
    **{m: "" for m in ["bisect", "collections", "functools", "heapq", "itertools", "math", "operator", "random",
        "re", "string", "sys"]},
}


def submission(src):
    quoted = "\n".join(f"# {ln}".rstrip() for ln in src.strip("\n").splitlines())
    return f"# mu {VERSION}\n{quoted}\n\n{transpile(src)}"


def preloads(py):
    """The import lines for the preloaded names py reads and does not bind
    itself (by an import, a def, a class or an assignment)."""
    tree = ast.parse(py)
    bound, read = set(), set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            (read if isinstance(node.ctx, ast.Load) else bound).add(node.id)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            bound.add(node.name)
        elif isinstance(node, ast.alias):
            bound.add((node.asname or node.name).split(".")[0])
        elif isinstance(node, ast.arg):
            bound.add(node.arg)
    needed = {}
    for name in sorted(read - bound):
        module = PRELOADS.get(name)
        if module is None:
            continue
        needed.setdefault(module or name, []).append(name if module else None)
    return [f"import {m}" if names == [None] else f"from {m} import {', '.join(names)}" for m, names in sorted(needed.items())]


def plain(src):
    py = transpile(src)
    lines = preloads(py)
    return "\n".join(lines) + "\n\n" + py if lines else py


def indent(line):
    return len(line) - len(line.lstrip())


def starter(py):
    lines = py.rstrip().split("\n")
    out = []
    for k, line in enumerate(lines):
        out.append(line)
        m = DEF.match(line)
        rest = [ln for ln in lines[k + 1 :] if ln.strip()]
        if m and (not rest or indent(rest[0]) <= indent(line)):
            out.append(m.group(1) + "    pass")
    return stub("\n".join(out) + "\n") or ""
