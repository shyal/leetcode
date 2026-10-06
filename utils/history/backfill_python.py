#!/usr/bin/env python3

# backfill_python - the python nodes, and the evidence for them mined from
# the solves already filed. The nodes follow The Python Tutorial
# (docs.python.org/3/tutorial), one node per section that names a
# construct, group "python". Each node has a detector over the ast of a
# solve: the class Solution and the top-level functions of a solved/ file,
# never the asserts under them. A solve whose code uses the construct
# gets the node added to its evidence record as "clean", with nothing
# else in the record touched: the solve was a pass (a FAILED file is
# skipped), the date is its date,
# the problem is its carrier, and the forgetting curve, breadth and the
# gauges read it like any other node. Files written in mu are skipped:
# their Python is the transpiler's output, not his typing.
#
#   utils/history/backfill_python.py          # dry run: counts per node
#   utils/history/backfill_python.py --apply  # write nodes.json and evidence.json
#
# Running it twice adds nothing the second time.

import argparse
import ast
import fcntl
import json
import os
import re
from typing import Callable, Dict, Iterable, List, Set

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
NODES = os.path.join(ROOT, "graph", "nodes.json")
EVIDENCE = os.path.join(ROOT, "graph", "evidence.json")
LOCK = os.path.join(ROOT, "graph", ".evidence.lock")
TUTORIAL = "https://docs.python.org/3/tutorial/"
ADDED = "2026-10-06"

Detector = Callable[[ast.AST], bool]

STR_METHODS = {
    "split",
    "join",
    "strip",
    "lstrip",
    "rstrip",
    "lower",
    "upper",
    "replace",
    "startswith",
    "endswith",
    "isdigit",
    "isalpha",
    "isalnum",
    "find",
    "count",
    "zfill",
    "title",
    "swapcase",
}
DICT_METHODS = {"get", "setdefault", "items", "keys", "values", "pop", "update"}
DUNDERS = {
    "__repr__",
    "__str__",
    "__eq__",
    "__lt__",
    "__hash__",
    "__len__",
    "__getitem__",
    "__contains__",
    "__call__",
}


def _call_name(node: ast.AST) -> str:
    """'enumerate' for enumerate(...), 'x.get' for x.get(...), '' otherwise."""
    if not isinstance(node, ast.Call):
        return ""
    f = node.func
    if isinstance(f, ast.Name):
        return f.id
    if isinstance(f, ast.Attribute):
        return "." + f.attr
    return ""


def _calls(name: str) -> Detector:
    return lambda n: _call_name(n) == name


def _method_in(names: Set[str]) -> Detector:
    return lambda n: _call_name(n).startswith(".") and _call_name(n)[1:] in names


def _module_use(module: str) -> Detector:
    """`re.search(...)` or `from re import ...` or `import re`."""

    def hit(n: ast.AST) -> bool:
        if isinstance(n, ast.Attribute):
            return isinstance(n.value, ast.Name) and n.value.id == module
        if isinstance(n, ast.Import):
            return any(a.name.split(".")[0] == module for a in n.names)
        if isinstance(n, ast.ImportFrom):
            return (n.module or "").split(".")[0] == module
        return False

    return hit


def _key_sort(n: ast.AST) -> bool:
    return _call_name(n) in ("sorted", ".sort", "max", "min") and any(
        k.arg == "key" for k in n.keywords  # type: ignore[attr-defined]
    )


def _nested_comp(n: ast.AST) -> bool:
    if not isinstance(n, (ast.ListComp, ast.SetComp)):
        return False
    return len(n.generators) > 1 or any(
        isinstance(c, (ast.ListComp, ast.GeneratorExp)) for c in ast.walk(n.elt)
    )


def _unpacking(n: ast.AST) -> bool:
    targets: List[ast.AST] = []
    if isinstance(n, ast.Assign):
        targets = list(n.targets)
    elif isinstance(n, (ast.For, ast.comprehension)):
        targets = [n.target]
    return any(isinstance(t, (ast.Tuple, ast.List)) for t in targets)


def _star_args(n: ast.AST) -> bool:
    if isinstance(n, ast.FunctionDef):
        return n.args.vararg is not None or n.args.kwarg is not None
    return isinstance(n, ast.Call) and any(isinstance(a, ast.Starred) for a in n.args)


def _keyword_call(n: ast.AST) -> bool:
    return isinstance(n, ast.Call) and any(
        k.arg not in (None, "key", "reverse", "default") for k in n.keywords
    )


def _user_class(n: ast.AST) -> bool:
    return isinstance(n, ast.ClassDef) and n.name != "Solution"


def _class_with_init(n: ast.AST) -> bool:
    return _user_class(n) and any(
        isinstance(b, ast.FunctionDef) and b.name == "__init__" for b in n.body  # type: ignore[attr-defined]
    )


def _subclass(n: ast.AST) -> bool:
    return _user_class(n) and bool(n.bases)  # type: ignore[attr-defined]


def _exception_class(n: ast.AST) -> bool:
    return isinstance(n, ast.ClassDef) and any(
        isinstance(b, ast.Name) and b.id.endswith(("Exception", "Error"))
        for b in n.bases
    )


def _decorated(name: str) -> Detector:
    def hit(n: ast.AST) -> bool:
        if not isinstance(n, (ast.ClassDef, ast.FunctionDef)):
            return False
        for d in n.decorator_list:
            d = d.func if isinstance(d, ast.Call) else d
            if (isinstance(d, ast.Name) and d.id == name) or (
                isinstance(d, ast.Attribute) and d.attr == name
            ):
                return True
        return False

    return hit


def _dunder(n: ast.AST) -> bool:
    return isinstance(n, ast.FunctionDef) and n.name in DUNDERS


def _iter_protocol(n: ast.AST) -> bool:
    return isinstance(n, ast.FunctionDef) and n.name in ("__iter__", "__next__")


def _chained(n: ast.AST) -> bool:
    return isinstance(n, ast.Compare) and len(n.ops) > 1


def _tuple_compare(n: ast.AST) -> bool:
    """(a, b) < (c, d): an ordering, not a membership test."""
    return (
        isinstance(n, ast.Compare)
        and isinstance(n.left, ast.Tuple)
        and all(isinstance(op, (ast.Lt, ast.LtE, ast.Gt, ast.GtE)) for op in n.ops)
    )


def _with_open(n: ast.AST) -> bool:
    """with open(...) as f: the builtin, not a local function named open."""
    return isinstance(n, ast.With) and any(
        _call_name(item.context_expr) == "open" for item in n.items
    )


def _loop_else(n: ast.AST) -> bool:
    return isinstance(n, (ast.For, ast.While)) and bool(n.orelse)


def _defaults(n: ast.AST) -> bool:
    return isinstance(n, ast.FunctionDef) and bool(
        n.args.defaults or n.args.kw_defaults
    )


def _isinst(*types: type) -> Detector:
    return lambda n: isinstance(n, types)


def _set_use(n: ast.AST) -> bool:
    return (
        isinstance(n, ast.SetComp) or _call_name(n) == "set" or isinstance(n, ast.Set)
    )


# (id, name, tutorial section, desc, hint, drill, detector)
NODE_TABLE = [
    (
        "py-slicing",
        "Slicing",
        "introduction.html#text",
        "s[1:4], s[::-1], s[-3:]: a slice is a copy; the end is exclusive; negative indices count from the end; s[i:j] on lists works the same.",
        "A prefix, a suffix, a window or a reversal of a sequence: a slice, never a loop that copies.",
        "Reverse each word of a sentence with slices.",
        _isinst(ast.Slice),
    ),
    (
        "py-str-methods",
        "String methods",
        "introduction.html#text",
        "s.split(), ' '.join(parts), s.strip(), s.lower(), s.replace(a, b), s.startswith(p): strings are immutable, every method returns a new one.",
        "Taking a string apart or putting one together: the method on str, and join on the separator.",
        "Normalise a sentence: lower, strip punctuation, single spaces.",
        _method_in(STR_METHODS),
    ),
    (
        "py-fstring",
        "f-strings",
        "inputoutput.html#formatted-string-literals",
        "f'{name}: {value:.2f}' with a format spec after the colon; f'{x=}' prints the name too; width and alignment with {v:>8}.",
        "Any text built from values: an f-string, never + and str().",
        "Format a table row with aligned columns.",
        _isinst(ast.JoinedStr),
    ),
    (
        "py-range",
        "range",
        "controlflow.html#the-range-function",
        "range(n), range(a, b), range(a, b, step), range(n - 1, -1, -1) to count down: a lazy sequence, exclusive at the end.",
        "A counted loop or a countdown: range with the right end and step.",
        "Every third index from the back.",
        _calls("range"),
    ),
    (
        "py-for-else",
        "else on a loop",
        "controlflow.html#else-clauses-on-loops",
        "for x in xs: ... if found: break / else: not found. The else runs when the loop ends without break.",
        "A search that must report 'none found': the else of the for, no flag variable.",
        "First divisor, or report prime, with for/else.",
        _loop_else,
    ),
    (
        "py-match",
        "match statement",
        "controlflow.html#match-statements",
        "match cmd: case ['go', direction]: ... case {'x': x, 'y': y}: ... case Point(x=0): ... case _: structural patterns bind names.",
        "Dispatch on the shape of a value, a list, a dict, a class: match, not a chain of isinstance.",
        "Parse a small command language with match.",
        _isinst(ast.Match),
    ),
    (
        "py-default-args",
        "Default argument values",
        "controlflow.html#default-argument-values",
        "def f(x, retries=3, memo=None): the default is evaluated once at definition time, so a mutable default is shared; use None and create inside.",
        "An optional parameter: a default value, and None for anything mutable.",
        "An accumulator function with a None default that is not shared.",
        _defaults,
    ),
    (
        "py-keyword-args",
        "Keyword arguments",
        "controlflow.html#keyword-arguments",
        "f(1, sep=', ', end=''): keyword arguments follow positional ones and can be given in any order; def f(a, /, b, *, c) fixes how each may be passed.",
        "A call with several optional settings: name them.",
        "Call a function with keyword arguments in a different order.",
        _keyword_call,
    ),
    (
        "py-star-args",
        "*args and **kwargs",
        "controlflow.html#arbitrary-argument-lists",
        "def f(*args, **kwargs) collects extras; f(*xs) and f(**d) unpack a sequence or a dict into a call.",
        "Forwarding or collecting any number of arguments: a star in the def or in the call.",
        "A wrapper that forwards every argument it is given.",
        _star_args,
    ),
    (
        "py-lambda",
        "Lambda expressions",
        "controlflow.html#lambda-expressions",
        "lambda p: p[1] is a one-expression function; used inline as a key or a callback.",
        "A tiny function used once, as an argument: a lambda.",
        "Sort pairs by their second element with a lambda key.",
        _isinst(ast.Lambda),
    ),
    (
        "py-sorted-key",
        "sort with a key",
        "datastructures.html#more-on-lists",
        "sorted(xs, key=len), xs.sort(key=lambda p: (-p[1], p[0])), max(d, key=d.get): the key is computed once per element; reverse=True flips.",
        "Ordering by something other than the value itself: key=, and a tuple key for a tie-break.",
        "Words by length, then alphabetically.",
        _key_sort,
    ),
    (
        "py-list-comprehension",
        "List comprehensions",
        "datastructures.html#list-comprehensions",
        "[f(x) for x in xs if ok(x)]: build a list in one expression; the if filters, the expression maps.",
        "A new list from an old one by map and filter: a comprehension, not append in a loop.",
        "Squares of the even numbers.",
        _isinst(ast.ListComp),
    ),
    (
        "py-nested-comprehension",
        "Nested comprehensions",
        "datastructures.html#nested-list-comprehensions",
        "[[row[i] for row in m] for i in range(n)] transposes; [x for row in m for x in row] flattens, loops left to right.",
        "A grid built or flattened in one expression: nest the fors in reading order.",
        "Transpose a matrix.",
        _nested_comp,
    ),
    (
        "py-tuple-unpacking",
        "Tuples and unpacking",
        "datastructures.html#tuples-and-sequences",
        "a, b = b, a; x, y = point; for i, (a, b) in enumerate(pairs); first, *rest = xs: the right side is packed, the left unpacks.",
        "Several values travel together: a tuple, and unpack them where they are used.",
        "Swap and rotate with unpacking.",
        _unpacking,
    ),
    (
        "py-sets",
        "Sets",
        "datastructures.html#sets",
        "set(xs), {x for x in xs}, a & b, a | b, a - b, x in s: no duplicates, no order, O(1) membership.",
        "Membership, duplicates, or what two collections share: a set.",
        "Words in both sentences.",
        _set_use,
    ),
    (
        "py-dict-methods",
        "Dictionary methods",
        "datastructures.html#dictionaries",
        "d.get(k, 0), d.setdefault(k, []).append(v), for k, v in d.items(), d.pop(k, None): a missing key is a default, not an error.",
        "Reading a key that may be missing: get or setdefault, never try/except KeyError.",
        "Group words by their first letter.",
        _method_in(DICT_METHODS),
    ),
    (
        "py-dict-comprehension",
        "Dict comprehensions",
        "datastructures.html#dictionaries",
        "{k: f(k) for k in keys}, {v: k for k, v in d.items()} inverts, dict(zip(keys, values)) pairs up.",
        "A mapping built from a sequence: a dict comprehension.",
        "Invert a mapping.",
        _isinst(ast.DictComp),
    ),
    (
        "py-enumerate",
        "enumerate",
        "datastructures.html#looping-techniques",
        "for i, x in enumerate(xs, start=1): the index and the element together; never range(len(xs)) with xs[i].",
        "A loop that needs the position too: enumerate.",
        "Positions of every element equal to its index.",
        _calls("enumerate"),
    ),
    (
        "py-zip",
        "zip",
        "datastructures.html#looping-techniques",
        "for a, b in zip(xs, ys): pairs in step, stops at the shorter; zip(*rows) transposes; strict=True refuses unequal lengths.",
        "Two sequences walked together: zip them.",
        "Dot product with zip.",
        _calls("zip"),
    ),
    (
        "py-chained-comparison",
        "Chained comparisons and conditions",
        "datastructures.html#more-on-conditions",
        "a < b <= c reads once and short-circuits; x = a or b takes the first truthy; in and not in test membership.",
        "A value inside a range: one chained comparison, no and.",
        "Is the point inside the box.",
        _chained,
    ),
    (
        "py-sequence-comparison",
        "Comparing sequences",
        "datastructures.html#comparing-sequences-and-other-types",
        "(1, 2, 'b') < (1, 2, 'c'): lexicographic, element by element, so a tuple is a ready-made sort key and a ready-made max.",
        "Ordering by several fields at once: compare the tuples.",
        "The latest version string by tuple comparison.",
        _tuple_compare,
    ),
    (
        "py-imports",
        "Modules and imports",
        "modules.html",
        "import math; from collections import deque; import numpy as np: a module is a namespace, imported once, and `if __name__ == '__main__':` guards a script.",
        "Something from the standard library: import the module, qualify the name.",
        "A module with a main guard and a function imported from it.",
        _isinst(ast.Import, ast.ImportFrom),
    ),
    (
        "py-files",
        "Reading and writing files",
        "inputoutput.html#reading-and-writing-files",
        "with open(path) as f: for line in f: ...; f.read(), f.write(s); the with closes it; mode 'w' truncates, 'a' appends.",
        "A file in or out: with open, iterate the lines.",
        "Count the words in a file.",
        _with_open,
    ),
    (
        "py-json",
        "json",
        "inputoutput.html#saving-structured-data-with-json",
        "json.dumps(obj, indent=2), json.loads(s), json.dump(obj, f), json.load(f): dicts, lists, str, numbers, bool and None round-trip.",
        "Data to or from text: json, never str() and eval().",
        "Round-trip a record through json and back.",
        _module_use("json"),
    ),
    (
        "py-try-except",
        "Handling exceptions",
        "errors.html#handling-exceptions",
        "try: ... except (ValueError, KeyError) as e: ... else: ... finally: ...: catch the narrowest type; else runs when nothing was raised.",
        "A call that can fail for a reason you can name: try, except that type, nothing broader.",
        "Parse what parses, skip what does not.",
        _isinst(ast.Try),
    ),
    (
        "py-raise",
        "Raising exceptions",
        "errors.html#raising-exceptions",
        "raise ValueError(f'bad {x!r}'); raise inside except re-raises; raise X from e chains.",
        "An input the function cannot honour: raise, with the type and a message.",
        "Validate an argument and raise.",
        _isinst(ast.Raise),
    ),
    (
        "py-custom-exception",
        "User-defined exceptions",
        "errors.html#user-defined-exceptions",
        "class InsufficientFunds(Exception): pass, with fields in __init__ when the handler needs them; callers catch the class.",
        "A failure the caller should be able to catch by name: your own Exception subclass.",
        "A bank account with its own exception.",
        _exception_class,
    ),
    (
        "py-with",
        "Context managers",
        "errors.html#predefined-clean-up-actions",
        "with open(p) as f, with lock:, with contextlib.suppress(FileNotFoundError): setup and guaranteed cleanup around a block.",
        "A resource that must be released whatever happens: with.",
        "A timer as a context manager.",
        _isinst(ast.With),
    ),
    (
        "py-class",
        "Classes",
        "classes.html#a-first-look-at-classes",
        "class Account: def __init__(self, owner, balance=0): self.owner = owner; methods take self; attributes live on the instance.",
        "State with behaviour attached: a class with __init__ and methods.",
        "A counter class with increment and reset.",
        _class_with_init,
    ),
    (
        "py-inheritance",
        "Inheritance",
        "classes.html#inheritance",
        "class Savings(Account): def __init__(...): super().__init__(...); a subclass overrides a method and calls super for the rest.",
        "A variant of an existing class: subclass it and override what differs.",
        "A savings account that extends an account.",
        _subclass,
    ),
    (
        "py-dunder-methods",
        "Special methods",
        "classes.html#odds-and-ends",
        "__repr__ for the debugger, __eq__ and __hash__ for sets and dict keys, __lt__ for sorting and heapq, __len__ and __getitem__ for a sequence.",
        "An object that should print, compare, sort or index like a built-in: the dunder for that protocol.",
        "A version class that sorts and prints.",
        _dunder,
    ),
    (
        "py-dataclass",
        "dataclasses",
        "classes.html#odds-and-ends",
        "@dataclass class Point: x: int; y: int = 0: __init__, __repr__ and __eq__ written for you; frozen=True makes it hashable; field(default_factory=list).",
        "A record of named fields: a dataclass, not a dict and not a hand-written __init__.",
        "An order line item as a dataclass with a computed total.",
        _decorated("dataclass"),
    ),
    (
        "py-iterator-protocol",
        "Iterators",
        "classes.html#iterators",
        "__iter__ returns self, __next__ returns the next value and raises StopIteration at the end; for calls both.",
        "Your own object in a for loop: __iter__ and __next__.",
        "A countdown iterator.",
        _iter_protocol,
    ),
    (
        "py-generator",
        "Generators",
        "classes.html#generators",
        "def chunks(xs, n): for i in range(0, len(xs), n): yield xs[i:i + n]: lazy, one value at a time, state kept between yields.",
        "A sequence produced on demand, or too big to hold: a generator with yield.",
        "Yield the running total of a stream.",
        _isinst(ast.Yield, ast.YieldFrom),
    ),
    (
        "py-generator-expression",
        "Generator expressions",
        "classes.html#generator-expressions",
        "sum(x * x for x in xs), max(len(w) for w in words), any(p(x) for x in xs): a comprehension without the list, fed straight to a consumer.",
        "A reduce over a mapped sequence: a generator expression inside sum, max, any, all.",
        "Sum of squares without a list.",
        _isinst(ast.GeneratorExp),
    ),
    (
        "py-regex",
        "re",
        "stdlib.html#string-pattern-matching",
        "re.findall(r'\\d+', s), re.sub(r'\\s+', ' ', s), m = re.match(p, s) and m.group(1): raw strings for patterns, compile what is reused.",
        "A text pattern with structure: re, with a raw string.",
        "Pull every date out of a log line.",
        _module_use("re"),
    ),
    (
        "py-datetime",
        "datetime",
        "stdlib.html#dates-and-times",
        "date.today(), datetime.strptime(s, '%Y-%m-%d'), d.strftime(...), (b - a).days, timedelta(days=7): aware datetimes carry tzinfo.",
        "Arithmetic on dates: datetime and timedelta, never string surgery.",
        "Days until the next birthday.",
        _module_use("datetime"),
    ),
    (
        "py-logging",
        "logging",
        "stdlib2.html#logging",
        "log = logging.getLogger(__name__); log.info('x=%s', x); logging.basicConfig(level=logging.INFO): levels, lazy formatting, one logger per module.",
        "Output a running program should leave behind: logging, not print.",
        "A function that logs at two levels.",
        _module_use("logging"),
    ),
]

DETECTORS: Dict[str, Detector] = {row[0]: row[6] for row in NODE_TABLE}


def python_nodes() -> List[dict]:
    """The nodes.json entries, in tutorial order."""
    return [
        {
            "id": nid,
            "group": "python",
            "added": ADDED,
            "name": name,
            "desc": desc,
            "hint": hint,
            "prereqs": [],
            "drill": drill,
            "source": TUTORIAL + section,
        }
        for nid, name, section, desc, hint, drill, _ in NODE_TABLE
    ]


def his_code(tree: ast.Module) -> Iterable[ast.AST]:
    """The class Solution and the top-level functions and classes: the code
    he wrote, without the asserts and the demo lines under it."""
    for node in tree.body:
        if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
            yield node


MU_BLOCK = re.compile(r"^# mu (\d+\.\d+|source)", re.M)


def constructs(source: str) -> Set[str]:
    """The python node ids a solve's code exercises; empty for a mu file
    or a file that does not parse."""
    if MU_BLOCK.search(source):
        return set()
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return set()
    found: Set[str] = set()
    for top in his_code(tree):
        for node in ast.walk(top):
            for nid, hit in DETECTORS.items():
                if nid not in found and hit(node):
                    found.add(nid)
    return found


def plan(evidence: dict) -> Dict[str, Set[str]]:
    """evidence key -> python nodes to add, for the .py solves on disk."""
    out: Dict[str, Set[str]] = {}
    for key, rec in evidence.items():
        if not key.endswith(".py") or "FAILED" in key:
            continue
        path = os.path.join(ROOT, key)
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as fh:
            found = constructs(fh.read())
        add = {n for n in found if n not in rec.get("moves", {})}
        if add:
            out[key] = add
    return out


def apply(additions: Dict[str, Set[str]]) -> None:
    with open(NODES) as fh:
        nodes = json.load(fh)
    have = {n["id"] for n in nodes["nodes"]}
    nodes["nodes"] += [n for n in python_nodes() if n["id"] not in have]
    with open(NODES, "w") as fh:
        json.dump(nodes, fh, indent=2)
        fh.write("\n")
    with open(LOCK, "a+") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        with open(EVIDENCE) as fh:
            ev = json.load(fh)
        for key, add in additions.items():
            moves = ev["evidence"][key].setdefault("moves", {})
            for nid in sorted(add):
                moves[nid] = "clean"
        with open(EVIDENCE, "w") as fh:
            json.dump(ev, fh, indent=2)
            fh.write("\n")


def main() -> None:
    ap = argparse.ArgumentParser(description="python nodes from the solves")
    ap.add_argument("--apply", action="store_true", help="write the graph files")
    args = ap.parse_args()
    with open(EVIDENCE) as fh:
        evidence = json.load(fh)["evidence"]
    additions = plan(evidence)
    per_node: Dict[str, int] = {nid: 0 for nid, *_ in NODE_TABLE}
    for add in additions.values():
        for nid in add:
            per_node[nid] += 1
    width = max(len(n) for n in per_node)
    for nid, count in per_node.items():
        print(f"{nid:<{width}}  {count:>5} solves")
    print(f"{len(additions)} records of {len(evidence)} gain a python node")
    if args.apply:
        apply(additions)
        print("wrote graph/nodes.json and graph/evidence.json")
    else:
        print("dry run; --apply writes graph/nodes.json and graph/evidence.json")


if __name__ == "__main__":
    main()
