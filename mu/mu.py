"""mu: a small language for LeetCode, transpiled to Python.

python mu/mu.py file.mu        print the Python for LeetCode
python mu/mu.py --version      print the language version

The language is specified in mu/spec/v<VERSION>.md.
"""

import re
import sys

VERSION = "0.5"

KEYWORDS = {"from", "in", "not", "and", "or", "if", "else", "is"}
# names that end a call written without brackets
NOT_ARGS = {"from", "in", "not", "and", "or", "if", "else", "is", "for", "while"}
NOT_ARGS |= {"elif", "def", "memo", "return", "del", "assert", "pass", "break"}
NOT_ARGS |= {"continue", "import", "extends"}
AUGMENTED = {
    "=",
    "+=",
    "-=",
    "*=",
    "/=",
    "//=",
    "%=",
    "**=",
    "&=",
    "|=",
    "^=",
    "<<=",
    ">>=",
}
FOLDS = {"sum", "max", "min", "count"}
CONSTANTS = {"true": "True", "false": "False", "none": "None"}

TOKEN = re.compile(
    r"(?P<ws>[ \t]+)"
    r"|(?P<comment>#.*)"
    r"|(?P<num>\d[\d_]*(?:\.\d[\d_]*)?(?:[eE][-+]?\d+)?)"
    r"|(?P<str>[fFrRbB]{0,2}'[^'\n]*'|[fFrRbB]{0,2}\"[^\"\n]*\")"
    r"|(?P<name>[A-Za-z_]\w*)"
    r"|(?P<op>\.\.<|\.\.|->|<-|//=|<<=|>>=|\*\*=|==|!=|<=|>=|\+=|-=|\*=|/=|%=|&=|\|=|\^="
    r"|<<|>>|//|\*\*|[-+*/%<>=()\[\]{},:|.&^~?])"
)


TRIPLE = re.compile(r"[fFrRbB]{0,2}('''|\"\"\")")


class MuError(Exception):
    def __init__(self, msg, eof=False):
        super().__init__(msg)
        self.eof = eof  # the input ended early: more lines may complete it


def triple(lines, k, pos):
    """The triple-quoted string that starts at lines[k][pos], which may run
    over several lines: (text, k, pos) with k and pos just past its closing
    quotes. None when no triple quote starts there."""
    m = TRIPLE.match(lines[k], pos)
    if not m:
        return None
    quote, first, parts, at = m.group(1), k, [], m.end()
    while True:
        end = lines[k].find(quote, at)
        if end >= 0:
            parts.append(lines[k][pos : end + 3])
            return "\n".join(parts), k, end + 3
        parts.append(lines[k][pos:])
        k, pos, at = k + 1, 0, 0
        if k == len(lines):
            raise MuError(f"line {first + 1}: unclosed {quote} string", eof=True)


def tokenize(src):
    """Tokens are (kind, value, line). Blocks are marked by INDENT and DEDENT."""
    toks, indents, depth = [], [0], 0
    lines, k = src.splitlines(), -1
    while k + 1 < len(lines):
        k += 1
        n, line = k + 1, lines[k]
        if depth == 0:
            body = line.strip()
            if not body or body.startswith("#"):
                continue
            ind = len(line) - len(line.lstrip(" "))
            if ind > indents[-1]:
                indents.append(ind)
                toks.append(("INDENT", "", n))
            while ind < indents[-1]:
                indents.pop()
                toks.append(("DEDENT", "", n))
            if ind != indents[-1]:
                raise MuError(f"line {n}: indentation does not match any block")
        pos = 0
        while pos < len(line):
            long = triple(lines, k, pos)
            if long:
                text, k, pos = long
                line = lines[k]
                toks.append(("STR", text, n))
                continue
            m = TOKEN.match(line, pos)
            if not m:
                raise MuError(f"line {n}: unexpected character {line[pos]!r}")
            pos = m.end()
            kind = m.lastgroup
            if kind in ("ws", "comment"):
                continue
            val = m.group()
            if val in "([{":
                depth += 1
            elif val in ")]}":
                depth -= 1
            toks.append((kind.upper(), val, n))
        if depth == 0 and toks and toks[-1][0] not in ("NEWLINE", "INDENT", "DEDENT"):
            toks.append(("NEWLINE", "", n))
    toks += [("DEDENT", "", 0)] * (len(indents) - 1) + [("EOF", "", 0)]
    return toks


class Py(str):
    """Python source for one expression, with facts the parser needs later."""

    div = None  # (a, b) when the expression is exactly a / b
    rng = None  # (lo, hi_exclusive) when the expression is a range
    parts = None  # the member types when a type is a parenthesized tuple
    call = False  # a call that dropped its brackets, `f x`
    convert = None  # the line after `int(a), b = ...` that converts a


HELPERS = {
    "Grid": (
        [],
        [],
        '''class Grid(list):
    """A list of rows that also takes a (row, col) pair as an index."""

    def __getitem__(self, k):
        if type(k) is tuple:
            return list.__getitem__(self, k[0])[k[1]]
        return list.__getitem__(self, k)

    def __setitem__(self, k, v):
        if type(k) is tuple:
            list.__getitem__(self, k[0])[k[1]] = v
        else:
            list.__setitem__(self, k, v)''',
    ),
    "deep": (
        ["import threading"],
        [],
        """def deep(fn):
    \"\"\"Run fn on a thread with a 256 MB stack, so deep memo recursion fits.\"\"\"
    out, err = [], []

    def target():
        try:
            out.append(fn())
        except BaseException as e:
            err.append(e)

    threading.stack_size(1 << 28)
    t = threading.Thread(target=target)
    t.start()
    t.join()
    if err:
        raise err[0]
    return out[0]""",
    ),
    # cells, nbrs, table, like, shape, put, pairs, levels, adjacency, indegrees copy the
    # utils/harness builtins; test_mu.py checks they agree
    "_holds": (
        [],
        [],
        """def _holds(v, eq=None, lt=None, lte=None, gt=None, gte=None):
    return (
        (eq is None or v == eq)
        and (lt is None or v < lt)
        and (lte is None or v <= lte)
        and (gt is None or v > gt)
        and (gte is None or v >= gte)
    )""",
    ),
    "cells": (
        [],
        ["_holds"],
        """def cells(grid, start=0, val=None, eq=None, lt=None, lte=None, gt=None, gte=None):
    eq = val if eq is None else eq
    for i in range(start, len(grid)):
        for j in range(start, len(grid[0])):
            if _holds(grid[i][j], eq, lt, lte, gt, gte):
                yield i, j""",
    ),
    "nbrs": (
        [],
        ["_holds"],
        """CARDINALS = ((-1, 0), (0, -1), (0, 1), (1, 0))


def nbrs(
    grid, r, c=None, dirs=CARDINALS, val=None, eq=None, lt=None, lte=None, gt=None, gte=None
):
    \"\"\"On-grid cells next to (r, c): up, left, right, down. nbrs(grid, p)
    takes the cell as one pair. With eq, lt, lte, gt or gte, only the cells
    whose value passes them all. val is the old name for eq.\"\"\"
    if c is None:
        r, c = r
    eq = val if eq is None else eq
    row = list.__getitem__ if isinstance(grid, list) else lambda g, i: g[i]
    m, n = len(grid), len(row(grid, 0))
    if dirs is CARDINALS:
        out = []
        if r > 0:
            out.append((r - 1, c))
        if c > 0:
            out.append((r, c - 1))
        if c + 1 < n:
            out.append((r, c + 1))
        if r + 1 < m:
            out.append((r + 1, c))
    else:
        out = [(r + dr, c + dc) for dr, dc in dirs if 0 <= r + dr < m and 0 <= c + dc < n]
    if eq is None and lt is None and lte is None and gt is None and gte is None:
        return out
    return [(i, j) for i, j in out if _holds(row(grid, i)[j], eq, lt, lte, gt, gte)]""",
    ),
    "table": (
        [],
        [],
        """def table(*dims, fill=0):
    if len(dims) == 1:
        return [fill] * dims[0]
    if len(dims) == 2:
        return [[fill] * dims[1] for _ in range(dims[0])]
    return [table(*dims[1:], fill=fill) for _ in range(dims[0])]""",
    ),
    "like": (
        [],
        ["table"],
        """def like(grid, fill=0):
    return table(len(grid), len(grid[0]), fill=fill)""",
    ),
    "shape": (
        [],
        [],
        """def shape(*seqs, last_index=False):
    if len(seqs) == 1:
        dims, x = [len(seqs[0])], seqs[0]
        while dims[-1] and isinstance(x[0], list):
            x = x[0]
            dims.append(len(x))
    else:
        dims = [len(s) for s in seqs]
    return tuple(d - 1 for d in dims) if last_index else tuple(dims)""",
    ),
    "put": (
        [],
        [],
        """def put(grid, at, v):
    for i, j in at:
        grid[i][j] = v""",
    ),
    "pairs": (
        [],
        [],
        """def pairs(n, type=tuple):
    for i in range(n):
        for j in range(i + 1, n):
            yield type((i, j))""",
    ),
    "levels": (
        [],
        ["_holds"],
        """def levels(
    q, grid=None, seen=None, grouped=False, eq=None, lt=None, lte=None, gt=None, gte=None
):
    bare = eq is None and lt is None and lte is None and gt is None and gte is None
    row = list.__getitem__ if isinstance(grid, list) else lambda g, i: g[i]
    d = 0
    while q:
        level = []
        for _ in range(len(q)):
            x = q.popleft()
            if seen is not None and x in seen:
                continue
            if not bare:
                v = x if grid is None else row(grid, x[0])[x[1]]
                if not _holds(v, eq, lt, lte, gt, gte):
                    continue
            if seen is not None:
                seen.add(x)
            if grouped:
                level.append(x)
            else:
                yield d, x
        if grouped and level:
            yield d, level
        d += 1""",
    ),
    "heap": (
        ["from heapq import heapify, heappop, heappush"],
        [],
        """class heap:
    class _Rev:
        __slots__ = "x"

        def __init__(self, x):
            self.x = x

        def __lt__(self, o):
            return o.x < self.x

    def __init__(self, items=(), type=min):
        self.rev = type is max
        self.h = [self.wrap(x) for x in items]
        heapify(self.h)

    def wrap(self, x):
        return heap._Rev(x) if self.rev else x

    def unwrap(self, x):
        return x.x if self.rev else x

    def push(self, x):
        heappush(self.h, self.wrap(x))

    append = push

    def pop(self):
        return self.unwrap(heappop(self.h))

    def peek(self):
        return self.unwrap(self.h[0])

    def __len__(self):
        return len(self.h)

    def __iter__(self):
        return (self.unwrap(x) for x in self.h)""",
    ),
    "adjacency": (
        ["from collections import defaultdict"],
        [],
        """def adjacency(edges, n=None, reverse=False, directed=True, weighted=False):
    adj = defaultdict(dict) if weighted else defaultdict(list)
    for c in range(n or 0):
        adj[c]
    for e in edges:
        a, b = e[:2]
        if reverse:
            a, b = b, a
        if weighted:
            adj[a][b] = e[2]
            if not directed:
                adj[b][a] = e[2]
        else:
            adj[a].append(b)
            if not directed:
                adj[b].append(a)
    return adj""",
    ),
    "indegrees": (
        ["from collections import defaultdict"],
        ["table"],
        """def indegrees(edges, n=None, reverse=False, directed=True, type=defaultdict):
    if type is list:
        if n is None:
            raise ValueError("type=list needs n")
        indeg = table(n)
    else:
        indeg = defaultdict(int)
        for c in range(n or 0):
            indeg[c]
    for e in edges:
        a, b = e[:2]
        if reverse:
            a, b = b, a
        indeg[b] += 1
        if not directed:
            indeg[a] += 1
    return indeg""",
    ),
    "components": (
        [],
        [],
        """def components(vertices, edges):
    left, out = set(vertices), []
    while left:
        stack, comp = [left.pop()], []
        while stack:
            u = stack.pop()
            comp.append(u)
            for v in edges(u):
                if v in left:
                    left.remove(v)
                    stack.append(v)
        out.append(comp)
    return out""",
    ),
    "graph": (
        [],
        [],
        """class Graph:
    def __init__(self, vertices, edges, directed=False):
        self.vertices = list(vertices)
        self.adj = {u: [] for u in self.vertices}
        for e in edges:
            u, v, w = e if len(e) == 3 else (*e, 1)
            self.adj[u].append((v, w))
            if not directed:
                self.adj[v].append((u, w))


def graph(vertices, edges, directed=False):
    return Graph(vertices, edges, directed)""",
    ),
    "dijkstra": (
        ["from heapq import heappop, heappush", "from math import inf"],
        [],
        """def dijkstra(g, src):
    dist = {u: inf for u in g.vertices}
    dist[src] = 0
    heap = [(0, src)]
    while heap:
        d, u = heappop(heap)
        if d > dist[u]:
            continue
        for v, w in g.adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heappush(heap, (d + w, v))
    return dist""",
    ),
}


class Parser:
    def __init__(self, src):
        self.toks = tokenize(src)
        self.i = 0
        self.imports = set()
        self.helpers = []
        self.memo_used = False
        self.folds = []  # (op, from, if, block) for each fold, for folds() in asserts

    # token helpers

    def peek(self, k=0):
        return self.toks[min(self.i + k, len(self.toks) - 1)]

    def at(self, val, k=0):
        t = self.peek(k)
        return t[1] == val and t[0] in ("OP", "NAME")

    def next(self):
        t = self.toks[self.i]
        self.i += 1
        return t

    def expect(self, val):
        t = self.next()
        if t[1] != val:
            got = t[1] or t[0]
            raise MuError(f"line {t[2]}: expected {val!r}, got {got!r}", t[0] == "EOF")
        return t

    def expect_kind(self, kind):
        t = self.next()
        if t[0] != kind:
            got = t[1] or t[0]
            raise MuError(
                f"line {t[2]}: expected {kind.lower()}, got {got!r}", t[0] == "EOF"
            )
        return t[1]

    def need(self, imp=None, helper=None):
        if imp:
            self.imports.add(imp)
        if helper and helper not in self.helpers:
            imps, deps, _ = HELPERS[helper]
            for d in deps:
                self.need(helper=d)
            self.imports.update(imps)
            self.helpers.append(helper)

    # statements

    def program(self):
        """imports, an optional `extends Base`, top-level assignments
        (constants, a Flag class), the defs of Solution, then a script: any
        statements, run after the class. Once the script starts, a def is a
        plain function, not a method."""
        defs, self.base, self.globals, self.script = [], None, [], []
        self.script_line = None  # where the script starts
        while self.peek()[0] != "EOF":
            t = self.peek()
            if self.script_line is None and (self.at("import") or self.at("from")):
                self.imports.add(self.import_line())
            elif self.script_line is None and self.at("extends"):
                self.next()
                self.base = self.expect_kind("NAME")
                self.expect_kind("NEWLINE")
            elif self.script_line is None and self.at("def"):
                defs.append(self.stmt())
            else:
                s = self.stmt()
                if not defs and s[0] == "assign":
                    self.globals.append(s)
                else:
                    if self.script_line is None:
                        self.script_line = t[2]
                    self.script.append(s)
        return defs

    def import_line(self):
        """`import a.b` or `from a.b import c, d`, passed through to Python."""
        words = []
        while self.peek()[0] != "NEWLINE":
            words.append(self.next()[1])
        self.next()
        return " ".join(words).replace(" . ", ".").replace(" ,", ",")

    def statements(self):
        """Any statements, for the REPL."""
        out = []
        while self.peek()[0] != "EOF":
            out.append(self.stmt())
        return out

    def block(self):
        """An indented block, or one statement after ':' on the same line."""
        if self.at(":"):
            self.next()
            return [self.simple()]
        self.expect_kind("NEWLINE")
        self.expect_kind("INDENT")
        body = []
        while self.peek()[0] != "DEDENT":
            body.append(self.stmt())
        self.next()
        return body

    def stmt(self):
        t = self.peek()
        if self.at("import") or self.at("from"):
            return ("import", self.import_line())
        if self.at("def"):
            return self.def_stmt()
        if self.at("memo") and self.peek(1)[0] == "NAME":
            return self.memo_stmt()
        if self.at("for"):
            self.next()
            it = self.repeat()
            if it is None:
                tgt, enum = self.target()
                self.expect("in")
                it = self.expr()
                it = f"enumerate({it})" if enum else it
            else:
                tgt = "_"
            return ("for", tgt, it, self.block(), self.loop_else())
        if self.at("while"):
            self.next()
            return ("while", self.expr(), self.block(), self.loop_else())
        if self.at("if"):
            arms = []
            self.next()
            arms.append((self.expr(), self.block()))
            while self.at("elif"):
                self.next()
                arms.append((self.expr(), self.block()))
            other = None
            if self.at("else"):
                self.next()
                other = self.block()
            return ("if", arms, other)
        if (
            t[1] in FOLDS
            and t[0] == "NAME"
            and (self.at("for", 1) or self.at("from", 1))
        ):
            head = self.fold(allow_block=True)
            if isinstance(head, tuple):
                return ("foldblock", *head, self.block())
            self.expect_kind("NEWLINE")
            return ("expr", head)
        if (
            self.at("ret")
            and self.peek(1)[0] == "NAME"
            and (self.at("=", 2) or self.at(",", 2))
        ):
            # `ret res = [first]`, `ret res, k = [], 0`: res is the def's
            # return value
            self.next()
            name = self.peek()[1]
            s = self.simple(newline=True)
            return ("assign", *s[1:], name)
        return self.simple(newline=True)

    def loop_else(self):
        """The block of a loop's `else`, run when the loop ends without break."""
        if self.at("else"):
            self.next()
            return self.block()
        return None

    def simple(self, newline=False):
        if self.at("return"):
            self.next()
            val = None if self.peek()[0] == "NEWLINE" else self.exprlist()
            s = ("return", val)
        elif self.at("break") or self.at("continue") or self.at("pass"):
            s = (self.next()[1],)
        elif self.at("del"):
            self.next()
            s = ("del", self.exprlist())
        elif self.at("assert"):
            self.next()
            s = ("assert", self.exprlist())
        else:
            lhs = self.exprlist()
            if self.at("<-"):
                # push: `stack <- x` appends x
                self.next()
                s = ("push", f"{lhs}.append({self.expr()})")
            elif self.peek()[1] in AUGMENTED and self.peek()[0] == "OP":
                op = self.next()[1]
                rhs = self.arg() if op == "=" and self.lambda_ahead() else self.exprlist()
                while op == "=" and self.at("="):
                    # chained: `a = b = 0` keeps every target in lhs
                    self.next()
                    lhs, rhs = Py(f"{lhs} = {rhs}"), self.exprlist()
                if op == "=":
                    lhs = converted(lhs)
                s = ("assign", lhs, op, rhs)
            else:
                s = ("expr", lhs)
        if newline or self.peek()[0] == "NEWLINE":
            self.expect_kind("NEWLINE")
        return s

    def def_stmt(self):
        self.expect("def")
        name = self.expect_kind("NAME")
        self.expect("(")
        params = []
        while not self.at(")"):
            p = self.expect_kind("NAME")
            t = None
            if self.at(":"):
                self.next()
                t = self.type()
            params.append((p, t))
            if not self.at(")"):
                self.expect(",")
        self.expect(")")
        ret = None
        if self.at("->"):
            self.next()
            ret = self.type()
        body = self.block()
        if len([s for s in body if ret_name([s])]) > 1:
            raise MuError(f"{name} has more than one ret line")
        if any(ret_name(b) for s in body for b in children(s)):
            raise MuError("a ret line must be a line of the def's own body")
        return ("def", name, params, ret, body)

    def memo_stmt(self):
        self.expect("memo")
        self.memo_used = True
        self.need("from functools import cache")
        self.need("import sys")
        self.need(helper="deep")
        name = self.expect_kind("NAME")
        self.expect("(")
        params = []
        while not self.at(")"):
            params.append(self.expect_kind("NAME"))
            if not self.at(")"):
                self.expect(",")
        self.expect(")")
        self.expect("=")
        cases = []
        if self.peek()[0] != "NEWLINE":
            cases.append((None, self.expr()))
            self.expect_kind("NEWLINE")
            return ("memo", name, params, cases)
        self.expect_kind("NEWLINE")
        self.expect_kind("INDENT")
        while self.at("|"):
            self.next()
            guard = None
            if self.at("else"):
                self.next()
            else:
                guard = self.expr()
            self.expect("->")
            cases.append((guard, self.expr()))
            self.expect_kind("NEWLINE")
        self.expect_kind("DEDENT")
        return ("memo", name, params, cases)

    def type(self):
        """[T] list, {K: V} dict, {T} set, (A, B) tuple, T? optional,
        A -> B or (A, B) -> C function; any other name passes through."""
        t = self.base_type()
        if self.at("->") and not self.at("NEWLINE", 1):
            self.next()
            self.need("from typing import Callable")
            args = ", ".join(t.parts) if t.parts is not None else t
            return Py(f"Callable[[{args}], {self.type()}]")
        return t

    def base_type(self):
        if self.at("["):
            self.next()
            inner = self.type()
            self.expect("]")
            t = Py(f"list[{inner}]")
        elif self.at("{"):
            self.next()
            key = self.type()
            if self.at(":"):
                self.next()
                t = Py(f"dict[{key}, {self.type()}]")
            else:
                t = Py(f"set[{key}]")
            self.expect("}")
        elif self.at("("):
            self.next()
            parts = [self.type()]
            while self.at(","):
                self.next()
                parts.append(self.type())
            self.expect(")")
            t = Py(f"tuple[{', '.join(parts)}]")
            t.parts = parts
        else:
            name = self.expect_kind("NAME")
            t = Py({"char": "str", "none": "None"}.get(name, name))
        if self.at("?"):
            self.next()
            self.need("from typing import Optional")
            t = Py(f"Optional[{t}]")
        return t

    def repeat(self):
        """`for xs` with no `in`: the iterable of a loop that names no
        variable, or None when a target and `in` follow."""
        start = self.i
        try:
            self.target()
            if self.at("in"):
                self.i = start
                return None
        except MuError:
            pass
        self.i = start
        return self.expr()

    def target(self):
        """`x`, `(a, b)`, or `i, x`; the last one enumerates."""
        first = self.pattern()
        if self.at(","):
            self.next()
            return f"{first}, {self.pattern()}", True
        return first, False

    def pattern(self):
        if self.at("("):
            self.next()
            parts = [self.pattern()]
            while self.at(","):
                self.next()
                parts.append(self.pattern())
            self.expect(")")
            return "(" + ", ".join(parts) + ")" if len(parts) > 1 else parts[0]
        return self.expect_kind("NAME")

    # expressions, lowest precedence first

    def exprlist(self):
        parts = [self.expr()]
        while self.at(","):
            self.next()
            parts.append(self.expr())
        return ", ".join(parts)

    def expr(self):
        e = self.or_()
        if self.at("if") and not self.at(":", 1):
            self.next()
            cond = self.or_()
            self.expect("else")
            return Py(f"{e} if {cond} else {self.expr()}")
        return e

    def or_(self):
        e = self.and_()
        while self.at("or"):
            self.next()
            e = Py(f"{e} or {self.and_()}")
        return e

    def and_(self):
        e = self.not_()
        while self.at("and"):
            self.next()
            e = Py(f"{e} and {self.not_()}")
        return e

    def not_(self):
        if self.at("not"):
            self.next()
            return Py(f"not {self.not_()}")
        return self.cmp()

    def cmp(self):
        e = self.range_()
        while True:
            if (
                self.peek()[1] in ("==", "!=", "<", ">", "<=", ">=")
                and self.peek()[0] == "OP"
            ):
                op = self.next()[1]
            elif self.at("in"):
                self.next()
                op = "in"
            elif self.at("not") and self.at("in", 1):
                self.i += 2
                op = "not in"
            elif self.at("is"):
                self.next()
                op = "is"
                if self.at("not"):
                    self.next()
                    op = "is not"
            else:
                return e
            e = Py(f"{e} {op} {self.range_()}")

    def range_(self):
        e = self.bitor()
        if self.at("..") or self.at("..<"):
            inclusive = self.next()[1] == ".."
            hi = self.bitor()
            end = f"{hi} + 1" if inclusive else hi
            r = Py(f"range({e}, {end})")
            r.rng = (e, end)
            return r
        return e

    def binary(self, ops, operand):
        e = operand()
        while self.peek()[1] in ops and self.peek()[0] == "OP":
            op = self.next()[1]
            e = Py(f"{e} {op} {operand()}")
        return e

    def bitor(self):
        return self.binary(("|",), self.bitxor)

    def bitxor(self):
        return self.binary(("^",), self.bitand)

    def bitand(self):
        return self.binary(("&",), self.shift)

    def shift(self):
        return self.binary(("<<", ">>"), self.arith)

    def arith(self):
        e = self.term()
        while self.peek()[1] in ("+", "-") and self.peek()[0] == "OP":
            op = self.next()[1]
            e = Py(f"{e} {op} {self.term()}")
        return e

    def term(self):
        e = self.unary()
        while self.peek()[1] in ("*", "/", "//", "%") and self.peek()[0] == "OP":
            op = self.next()[1]
            rhs = self.unary()
            a = e
            e = Py(f"{e} {op} {rhs}")
            if op == "/":
                e.div = (a, rhs)
        return e

    def unary(self):
        if self.at("-") or self.at("~"):
            op = self.next()[1]
            return Py(f"{op}{self.unary()}")
        e = self.postfix()
        if self.at("**"):
            self.next()
            return Py(f"{e} ** {self.unary()}")
        return e

    def operand_next(self):
        """The next token can start an argument of a call without brackets."""
        t = self.peek()
        if t[0] in ("NUM", "STR"):
            return True
        if t[0] != "NAME" or t[1] in NOT_ARGS:
            return False
        if t[1] in FOLDS and (self.at("for", 1) or self.at("from", 1)):
            return False
        return not (t[1] == "first" and self.at("in", 2))

    def postfix(self, nested=False):
        """A call may drop its brackets when it has one argument: `f x` is
        f(x), `print len xs` is print(len(xs)), and it binds tighter than any
        operator, so `len xs - 1` is len(xs) - 1.

        A `for` after the argument makes it a generator: `set f y for y in
        xs` is set(f(y) for y in xs). The innermost call `f y` is the
        generator's element, so it leaves the `for` to the call around it."""
        named = self.peek()[0] == "NAME"
        e = self.postfix_chain()
        if named and self.operand_next():
            arg = self.postfix(nested=True)
            if self.at("for") and (arg.call or not nested):
                arg = Py(f"{arg}{self.comprehension()}")
            out = self.special(e, [arg], [])
            out.call = True
            return out
        return e

    def postfix_chain(self):
        e = self.primary()
        while True:
            if self.at("("):
                e = self.call(e)
            elif self.at("["):
                self.next()
                idx = self.subscript()
                self.expect("]")
                e = Py(f"{e}[{idx}]")
            elif self.at("."):
                self.next()
                if self.peek()[0] == "NAME" and self.peek()[1] not in STATEMENT_WORDS:
                    e = Py(f"{e}.{self.next()[1]}")
                else:
                    e = Py(f"{e}.pop()")  # pop: `stack .` removes the last item
            else:
                return e

    def subscript(self):
        """An index `i`, `i, j`, or a slice `lo:hi:step` with parts optional."""
        parts, cur = [], None
        while True:
            if self.at(":"):
                self.next()
                parts.append(cur or "")
                cur = None
            elif self.at("]"):
                parts.append(cur or "")
                break
            else:
                cur = self.exprlist()
        return ":".join(parts)

    def primary(self):
        t = self.peek()
        kind, val = t[0], t[1]
        if kind in ("NUM", "STR"):
            self.next()
            return Py(val)
        if kind == "NAME":
            if val in FOLDS and (self.at("for", 1) or self.at("from", 1)):
                return self.fold()
            if val == "first" and self.peek(1)[0] == "NAME" and self.at("in", 2):
                return self.first()
            if val in KEYWORDS:
                raise MuError(f"line {t[2]}: unexpected {val!r}")
            self.next()
            if val == "inf":
                self.need("from math import inf")
            return Py(CONSTANTS.get(val, val))
        if val == "(":
            self.next()
            if self.at(")"):
                self.next()
                return Py("()")
            parts = [self.expr()]
            if self.at("for"):  # a generator: (e for x in xs)
                gen = self.comprehension()
                self.expect(")")
                return Py(f"({parts[0]}{gen})")
            one = False  # (x,) is a one-element tuple
            while self.at(","):
                self.next()
                if self.at(")"):
                    one = len(parts) == 1
                    break
                parts.append(self.expr())
            self.expect(")")
            return Py(f"({', '.join(parts)}{',' if one else ''})")
        if val == "[":
            return self.collection("[", "]")
        if val == "{":
            return self.collection("{", "}")
        raise MuError(f"line {t[2]}: unexpected {val or kind!r}")

    def collection(self, open_, close):
        self.expect(open_)
        if self.at(close):
            self.next()
            return Py(open_ + close)
        first = self.item(open_)
        if self.at("for"):
            gen = self.comprehension()
            self.expect(close)
            return Py(f"{open_}{first}{gen}{close}")
        items = [first]
        while self.at(","):
            self.next()
            if self.at(close):
                break
            items.append(self.item(open_))
        self.expect(close)
        return Py(open_ + ", ".join(items) + close)

    def item(self, open_):
        if self.at("*"):
            self.next()
            return Py(f"*{self.expr()}")
        e = self.expr()
        if open_ == "{" and self.at(":"):
            self.next()
            e = Py(f"{e}: {self.expr()}")
        return e

    def comprehension(self):
        """One or more `for target in iter [if cond]` clauses."""
        out = ""
        while self.at("for"):
            self.next()
            tgt, enum = self.target()
            self.expect("in")
            it = self.or_()
            out += f" for {tgt} in {f'enumerate({it})' if enum else it}"
            while self.at("if"):
                self.next()
                out += f" if {self.or_()}"
        return out

    def call(self, fn):
        self.expect("(")
        args, kwargs = [], []
        while not self.at(")"):
            if self.peek()[1] in ("+", "*") and self.peek(1)[1] in (",", ")"):
                args.append(Py(self.next()[1]))
            elif self.at("*"):
                self.next()
                args.append(Py(f"*{self.expr()}"))
            elif self.peek()[0] == "NAME" and self.at("=", 1):
                k = self.next()[1]
                self.next()
                kwargs.append((k, self.arg()))
            else:
                args.append(self.arg())
            if not self.at(")"):
                self.expect(",")
        self.expect(")")
        return self.special(fn, args, kwargs)

    def lambda_ahead(self):
        """Whether `x ->` or `(a, b) ->` starts here."""
        if self.peek()[0] == "NAME":
            return self.at("->", 1)
        if not self.at("("):
            return False
        j, depth = self.i, 0
        while True:
            v = self.toks[j][1]
            depth += v == "("
            depth -= v == ")"
            j += 1
            if depth == 0 or self.toks[j][0] in ("NEWLINE", "EOF"):
                break
        return depth == 0 and self.toks[j][1] == "->"

    def arg(self):
        """A call argument or the value of `f = x -> e`: the two places a
        lambda may appear."""
        if self.peek()[0] == "NAME" and self.at("->", 1):
            name = self.next()[1]
            self.next()
            return Py(f"lambda {name}: {self.expr()}")
        if self.at("("):
            if self.lambda_ahead():
                self.next()
                names = []
                while not self.at(")"):
                    names.append(self.expect_kind("NAME"))
                    if not self.at(")"):
                        self.expect(",")
                self.expect(")")
                self.expect("->")
                if not names:  # () -> e takes nothing: defaultdict(() -> [0, 0])
                    return Py(f"lambda: {self.expr()}")
                names = [f"_{k}" if n == "_" else n for k, n in enumerate(names)]
                # (a, b) -> e takes a and b, or one pair it unpacks
                inner = f"(lambda {', '.join(names)}: {self.expr()})"
                return Py(f"lambda *_a: {inner}(*(_a[0] if len(_a) == 1 else _a))")
        e = self.expr()
        if self.at("for"):
            return Py(f"{e}{self.comprehension()}")
        return e

    def special(self, fn, args, kwargs):
        kw = {k: v for k, v in kwargs}
        if fn == "ceil" and len(args) == 1 and args[0].div:
            a, b = args[0].div
            return Py(f"-(-({a}) // ({b}))")
        if fn == "floor" and len(args) == 1 and args[0].div:
            a, b = args[0].div
            return Py(f"({a}) // ({b})")
        if fn == "sort":
            if "by" in kw:
                kw["key"] = kw.pop("by")
            fn = "sorted"
        if fn == "scan":
            self.need("from itertools import accumulate")
            op, xs = args
            if op == "+":
                return Py(f"accumulate({xs})")
            if op == "*":
                self.need("import operator")
                op = "operator.mul"
            return Py(f"accumulate({xs}, {op})")
        if fn == "counter":
            self.need("from collections import Counter")
            fn = "Counter"
        if fn in ("ceil", "floor"):
            self.need(f"from math import {fn}")
        if fn in HELPERS:
            self.need(helper=fn)
        parts = list(args) + [f"{k}={v}" for k, v in kw.items()]
        return Py(f"{fn}({', '.join(parts)})")

    def fold(self, allow_block=False):
        """sum|max|min|count [from e] for target in iter [if cond] (: body | block)."""
        op = self.next()[1]
        start = None
        if self.at("from"):
            self.next()
            start = self.arith()
        self.expect("for")
        tgt, enum = self.target()
        self.expect("in")
        it = self.or_()
        it = f"enumerate({it})" if enum else it
        where = None
        if self.at("if"):
            self.next()
            where = self.or_()
        block = (
            allow_block and self.peek()[0] == "NEWLINE" and self.peek(1)[0] == "INDENT"
        )
        self.folds.append((op, start is not None, where is not None, block))
        if block:
            return (op, start, tgt, it, where)
        body = None
        if self.at(":"):
            self.next()
            body = self.expr()
        cond = f" if {where}" if where else ""
        if op == "count":
            test = " and ".join(f"({c})" for c in (where, body) if c)
            gen = f"1 for {tgt} in {it}" + (f" if {test}" if test else "")
            return Py(f"({start} + sum({gen}))" if start else f"sum({gen})")
        if body is None:
            raise MuError(f"line {self.peek()[2]}: {op} for needs ': value' or a block")
        gen = f"{body} for {tgt} in {it}{cond}"
        if op == "sum":
            return Py(f"({start} + sum({gen}))" if start else f"sum({gen})")
        if start is None:
            return Py(f"{op}({gen})")
        return Py(f"{op}({start}, {op}(({gen}), default={start}))")

    def first(self):
        """first k in lo..hi if pred: the least k with pred true (pred monotone)."""
        self.expect("first")
        k = self.expect_kind("NAME")
        self.expect("in")
        rng = self.range_()
        if not rng.rng:
            raise MuError(f"line {self.peek()[2]}: first needs a range lo..hi")
        self.expect("if")
        pred = self.expr()
        self.need("from bisect import bisect_left")
        lo = rng.rng[0]
        return Py(f"{lo} + bisect_left({rng}, True, key=lambda {k}: {pred})")


NAME = re.compile(r"[A-Za-z_]\w*")


def split_top(text):
    """Split at commas outside brackets."""
    parts, depth, cur = [], 0, ""
    for ch in text:
        depth += (ch in "([{") - (ch in ")]}")
        if ch == "," and depth == 0:
            parts.append(cur.strip())
            cur = ""
        else:
            cur += ch
    return parts + [cur.strip()]


CONVERT = re.compile(r"([A-Za-z_][\w.]*)\(([A-Za-z_]\w*)\)")


def converted(lhs):
    """`int(a), b = ...` assigns a and b, then passes a through int. The
    left side comes back as `a, b`, with the second line in `convert`."""
    parts = split_top(lhs)
    calls = [(p, CONVERT.fullmatch(p)) for p in parts]
    if " = " in lhs or not any(m for _, m in calls):
        return lhs
    out = Py(", ".join(m.group(2) if m else p for p, m in calls))
    names = ", ".join(m.group(2) for _, m in calls if m)
    out.convert = f"{names} = {', '.join(p for p, m in calls if m)}"
    return out


def targets(lhs):
    """The plain names an assignment's left side binds: `a, b = c = ...`."""
    return {
        t for side in lhs.split(" = ") for t in split_top(side) if NAME.fullmatch(t)
    }


def assigned(stmts):
    """Plain names a block assigns with = or op=, not inside nested defs."""
    out = set()
    for s in stmts:
        if s[0] == "assign":
            out |= targets(s[1])
        for body in children(s):
            out |= assigned(body)
    return out


def bound(stmts):
    """Every name a block binds: assignments, loop targets, defs."""
    out = set()
    for s in stmts:
        if s[0] == "assign":
            out |= targets(s[1])
        elif s[0] in ("def", "memo"):
            out.add(s[1])
        elif s[0] == "for":
            out |= set(NAME.findall(s[1]))
        elif s[0] == "foldblock":
            out |= set(NAME.findall(s[3]))
        for body in children(s):
            out |= bound(body)
    return out


def ret_name(stmts):
    """The name a `ret` line of this block declares, or None."""
    for s in stmts:
        if s[0] == "assign" and len(s) == 5:
            return s[4]
    return None


def children(s):
    """The blocks inside a statement, except a nested def's own body."""
    if s[0] == "for":
        return [s[3]] + ([s[4]] if s[4] else [])
    if s[0] == "while":
        return [s[2]] + ([s[3]] if s[3] else [])
    if s[0] == "if":
        return [b for _, b in s[1]] + ([s[2]] if s[2] else [])
    if s[0] == "foldblock":
        return [s[6]]
    return []


class Emitter:
    """Writes Python. A block's last value goes through the format string
    `last`: "return {}" in a def, something else at the REPL's top level.
    A nested def that assigns a name an enclosing def binds gets `nonlocal`."""

    def __init__(self, method=True):
        self.lines = []
        self.fresh = 0
        self.method = method
        self.scopes = []  # names bound by each enclosing def
        self.rets = []  # the ret name of each enclosing def, or None

    def out(self, ind, s):
        self.lines.append("    " * ind + s)

    def block(self, stmts, ind, returns=False):
        for k, s in enumerate(stmts):
            self.stmt(s, ind, returns if k == len(stmts) - 1 else False)

    def stmt(self, s, ind, last):
        kind = s[0]
        if kind == "def":
            self.def_(s, ind)
        elif kind == "memo":
            _, name, params, cases = s
            self.out(ind, "@cache")
            self.out(ind, f"def {name}({', '.join(params)}):")
            for guard, val in cases:
                if guard is None:
                    self.out(ind + 1, f"return {val}")
                else:
                    self.out(ind + 1, f"if {guard}:")
                    self.out(ind + 2, f"return {val}")
        elif kind == "for":
            _, tgt, it, body, other = s
            self.out(ind, f"for {tgt} in {it}:")
            self.block(body, ind + 1)
            self.loop_else(other, ind)
        elif kind == "while":
            self.out(ind, f"while {s[1]}:")
            self.block(s[2], ind + 1)
            self.loop_else(s[3], ind)
        elif kind == "if":
            _, arms, other = s
            for k, (cond, body) in enumerate(arms):
                self.out(ind, f"{'if' if k == 0 else 'elif'} {cond}:")
                self.block(body, ind + 1, returns=last)
            if other:
                self.out(ind, "else:")
                self.block(other, ind + 1, returns=last)
        elif kind == "assign":
            self.out(ind, f"{s[1]} {s[2]} {s[3]}")
            if getattr(s[1], "convert", None):
                self.out(ind, s[1].convert)
        elif kind == "return":
            val = s[1] if s[1] is not None else (self.rets or [None])[-1]
            self.out(ind, "return" if val is None else f"return {val}")
        elif kind in ("break", "continue", "pass"):
            self.out(ind, kind)
        elif kind in ("import", "push"):
            self.out(ind, s[1])
        elif kind == "del":
            self.out(ind, f"del {s[1]}")
        elif kind == "assert":
            self.out(ind, f"assert {s[1]}")
        elif kind == "expr":
            self.out(ind, last.format(s[1]) if last else s[1])
        elif kind == "foldblock":
            self.foldblock(s, ind, last)

    def loop_else(self, other, ind):
        if other:
            self.out(ind, "else:")
            self.block(other, ind + 1)

    def def_(self, s, ind):
        _, name, params, ret, body = s
        top = not self.scopes  # a method of Solution, or a REPL function
        names = {p for p, _ in params}
        sig = ["self"] * (self.method and top)
        sig += [p if t is None else f"{p}: {t}" for p, t in params]
        arrow = f" -> {ret}" if ret else ""
        self.out(ind, f"def {name}({', '.join(sig)}){arrow}:")
        if self.scopes:
            shared = assigned(body) & set().union(*self.scopes) - names
            if shared:
                self.out(ind + 1, f"nonlocal {', '.join(sorted(shared))}")
        grids = []
        if top:
            for p, t in params:
                if t and t.startswith("list[list["):
                    grids.append(p)
                    self.out(ind + 1, f"_in_{p}, {p} = {p}, Grid({p})")
                    self.out(ind + 1, f"_w_{p} = {p}")
        if grids:
            # the rows go back into the caller's list, so an in-place
            # sort, reverse or append on the grid reaches the caller
            self.out(ind + 1, "try:")
            ind += 1
        self.scopes.append(names | bound(body))
        res = ret_name(body)
        self.rets.append(res)
        returns = False if res else "return {}"
        if top and any(b[0] == "memo" for b in body):
            # memo recursion can run 10^4+ deep: evaluate on a big stack
            self.out(ind + 1, "def run():")
            shared = assigned(body) & names
            if shared:
                self.out(ind + 2, f"nonlocal {', '.join(sorted(shared))}")
            self.block(body, ind + 2, returns=returns)
            if res:
                self.out(ind + 2, f"return {res}")
            self.out(ind + 1, "return deep(run)")
        else:
            self.block(body, ind + 1, returns=returns)
            if res:
                self.out(ind + 1, f"return {res}")
        self.scopes.pop()
        self.rets.pop()
        if grids:
            self.out(ind, "finally:")
            for p in grids:
                self.out(ind + 1, f"_in_{p}[:] = _w_{p}")

    def foldblock(self, s, ind, last):
        _, op, start, tgt, it, where, body = s
        if not body or body[-1][0] != "expr":
            raise MuError(f"the last line of a {op} for block must be a value")
        self.fresh += 1
        acc = "acc" if self.fresh == 1 else f"acc{self.fresh}"
        if start is None:
            start = "0" if op in ("sum", "count") else "None"
        self.out(ind, f"{acc} = {start}")
        self.out(ind, f"for {tgt} in {it}:")
        if where:
            self.out(ind + 1, f"if not ({where}):")
            self.out(ind + 2, "continue")
        self.block(body[:-1], ind + 1)
        val = body[-1][1]
        if op == "sum":
            self.out(ind + 1, f"{acc} += {val}")
        elif op == "count":
            self.out(ind + 1, f"{acc} += bool({val})")
        elif start == "None":
            self.out(ind + 1, f"{acc} = {val} if {acc} is None else {op}({acc}, {val})")
        else:
            self.out(ind + 1, f"{acc} = {op}({acc}, {val})")
        if last:
            self.out(ind, last.format(acc))


def transpile(src):
    p = Parser(src)
    defs = p.program()
    if any(t and t.startswith("list[list[") for d in defs for _, t in d[2]):
        p.need(helper="Grid")
    e = Emitter()
    for g in p.globals:
        e.stmt(g, 0, False)
    if p.globals:
        e.out(0, "\n")
    e.out(0, f"class Solution({p.base}):" if p.base else "class Solution:")
    for k, d in enumerate(defs):
        if k:
            e.out(0, "")
        e.stmt(d, 1, False)
    parts = []
    if p.imports:
        parts.append("\n".join(sorted(p.imports)))
    if p.memo_used:
        parts.append("sys.setrecursionlimit(1 << 20)")
    parts += [HELPERS[h][2] for h in p.helpers]
    parts.append("\n".join(e.lines))
    if p.script:
        script = Emitter(method=False)  # a def here is a plain function
        script.block(p.script, 0)
        parts.append("\n".join(script.lines))
    return "\n\n\n".join(parts) + "\n"


def compile_stmts(src, last="_ = {}"):
    """Top-level statements to Python, for the REPL: (imports, helpers, code).
    The value of a final expression goes through `last`."""
    p = Parser(src)
    stmts = p.statements()
    defs = [s for s in stmts if s[0] == "def"]
    if any(t and t.startswith("list[list[") for d in defs for _, t in d[2]):
        p.need(helper="Grid")
    e = Emitter(method=False)
    e.block(stmts, 0, returns=last)
    return sorted(p.imports), list(p.helpers), "\n".join(e.lines) + "\n"


# formatter

STATEMENT_WORDS = {
    "def", "memo", "for", "in", "if", "elif", "else", "while", "return", "and",
    "or", "not", "from", "first", "break", "continue",
}  # fmt: skip
TIGHT = {"..", "..<", "."}


def gap(prev, cur, unary, subscript, paren=False):
    """The spacing written between two tokens on one line. Inside round
    brackets `=` names an argument and is tight: f(xs, by=key)."""
    (pk, pv), (ck, cv) = prev, cur
    if paren and "=" in (pv, cv) and "OP" in (pk, ck):
        if (pk, pv) == ("OP", "=") or (ck, cv) == ("OP", "="):
            return ""
    if ck == "COMMENT" or ck == "POP":
        return "  " if ck == "COMMENT" else " "
    if ck == "OP" and cv in (",", ":", ")", "]", "}", "?"):
        return ""
    if pk == "OP" and pv in "([{":
        return ""
    if cv in TIGHT or pv in TIGHT or unary:
        return ""
    if subscript and pk == "OP" and pv == ":":
        return ""  # a slice: a[i:j], a[::-1]
    if ck == "OP" and cv in "([":
        if pk in ("NUM", "STR") or (pk == "NAME" and pv not in STATEMENT_WORDS):
            return ""
        if pk == "OP" and pv in ")]}?":
            return ""
    return " "


def pop_dots(toks):
    """A `.` not followed by a plain name is a pop; mark it so the
    formatter keeps it apart: `stack .`, never `stack.`."""
    out = list(toks)
    for k, t in enumerate(toks):
        nxt = toks[k + 1] if k + 1 < len(toks) else None
        attribute = nxt and nxt[0] == "NAME" and nxt[1] not in STATEMENT_WORDS
        if t == ("OP", ".") and not attribute:
            out[k] = ("POP", ".")
    return out


def render(toks):
    out, prev, unary, stack = [], None, False, []
    for t in pop_dots(toks):
        pk, pv = prev or ("OP", "(")
        if prev is not None:
            sub = bool(stack) and stack[-1] is True
            out.append(gap(prev, t, unary, sub, bool(stack) and stack[-1] == "("))
        if t[0] == "OP" and t[1] in "([{":
            # `[` right after a value opens a subscript, where `:` is tight
            after_value = pk in ("NAME", "NUM", "STR") and pv not in STATEMENT_WORDS
            after_value = after_value or pk == "OP" and pv in ")]}"
            sub = t[1] == "[" and prev is not None and after_value
            stack.append(True if sub else t[1])
        elif t[0] == "OP" and t[1] in ")]}" and stack:
            stack.pop()
        opens = prev is None or pk == "OP" and pv not in ")]}" or pv in STATEMENT_WORDS
        unary = t[0] == "OP" and (
            t[1] in ("-", "~")
            and opens
            or t[1] == "*"
            and (prev is None or pv in "([{,")
        )
        out.append(t[1])
        prev = t
    return "".join(out)


BLOCK_WORDS = {"if", "elif", "else", "for", "while"}


def split_inline(toks):
    """(header, body) for `if cond: stmt` and the like, so the body goes on
    its own line; (toks, []) when the line has no one-line body. The block
    colon is the first one outside brackets that no fold (`sum for x in
    xs: e`) on the line claims."""
    if not toks or toks[0][0] != "NAME" or toks[0][1] not in BLOCK_WORDS:
        return toks, []
    depth, folds = 0, 0
    for k, (kind, val) in enumerate(toks):
        if kind == "OP" and val in "([{":
            depth += 1
        elif kind == "OP" and val in ")]}":
            depth -= 1
        elif depth == 0 and kind == "NAME" and val in FOLDS and k + 1 < len(toks):
            folds += toks[k + 1][1] in ("for", "from")
        elif depth == 0 and (kind, val) == ("OP", ":"):
            if folds:
                folds -= 1
                continue
            body = toks[k + 1 :]
            if not body or body[0][0] == "COMMENT":
                return toks, []
            return toks[:k], body
    return toks, []


def top_arrow(text):
    """Index of the first ` -> ` outside brackets, or -1."""
    depth = 0
    for i, ch in enumerate(text):
        depth += ch in "([{"
        depth -= ch in ")]}"
        if depth == 0 and text.startswith(" -> ", i):
            return i
    return -1


def align_cases(lines):
    """Pad the guards of consecutive `| guard -> value` lines to one width."""
    i = 0
    while i < len(lines):
        j = i
        while j < len(lines) and lines[j] and lines[j][1].startswith("| "):
            j += 1
        run = [k for k in range(i, j) if top_arrow(lines[k][1]) >= 0]
        if run:
            width = max(top_arrow(lines[k][1]) for k in run)
            for k in run:
                level, text = lines[k]
                a = top_arrow(text)
                lines[k] = (level, text[:a].ljust(width) + text[a:])
        i = max(j, i + 1)
    return lines


def fmt(src):
    """Reprint a mu program: two-space blocks, one space around binary
    operators, no space in ranges, `->` aligned down a memo's cases, one
    blank line between top-level defs, and every one-line body (`if c: x`)
    moved onto its own indented line. A bracketed expression split over
    several lines is joined into one. fmt(fmt(s)) == fmt(s)."""
    lines, indents, buf, depth, blank, level = [], [0], [], 0, False, 0
    rows, k = src.splitlines(), -1
    while k + 1 < len(rows):
        k += 1
        n, line = k + 1, rows[k]
        if depth == 0:
            body = line.strip()
            if not body:
                blank = bool(lines)
                continue
            ind = len(line) - len(line.lstrip(" "))
            if body.startswith("#"):
                # a comment opening a block sits one level in
                level = sum(1 for d in indents[1:] if d <= ind) + (ind > indents[-1])
            else:
                if ind > indents[-1]:
                    indents.append(ind)
                while ind < indents[-1]:
                    indents.pop()
                if ind != indents[-1]:
                    raise MuError(f"line {n}: indentation does not match any block")
                level = len(indents) - 1
            # a top-level def gets a blank line above it and its comments
            top = level == 0 and (body.startswith("def ") or body.startswith("#"))
            after_comment = lines and lines[-1] and lines[-1][1].startswith("#")
            if lines and (blank or top and lines[-1] is not None and not after_comment):
                lines.append(None)
            blank = False
        pos = 0
        while pos < len(line):
            long = triple(rows, k, pos)
            if long:
                text, k, pos = long
                line = rows[k]
                buf.append(("STR", text))
                continue
            m = TOKEN.match(line, pos)
            if not m:
                raise MuError(f"line {n}: unexpected character {line[pos]!r}")
            pos = m.end()
            if m.lastgroup == "ws":
                continue
            val = m.group()
            if m.lastgroup == "op":
                depth += (val in "([{") - (val in ")]}")
            buf.append((m.lastgroup.upper(), val))
        if depth == 0 and buf:
            at = level
            while buf:  # `if c: stmt` becomes a header and an indented body
                head, buf = split_inline(buf)
                lines.append((at, render(head)))
                at += 1
    if depth:
        raise MuError("unclosed bracket at end of file")
    lines = align_cases(lines)
    text = ["" if ln is None else "  " * ln[0] + ln[1] for ln in lines]
    return "\n".join(text).strip("\n") + "\n"


if __name__ == "__main__":
    args = sys.argv[1:]
    if args == ["--version"]:
        sys.exit(print(f"mu {VERSION}"))
    run = transpile
    if args[:1] == ["--fmt"]:
        run, args = fmt, args[1:]
    if len(args) != 1:
        sys.exit(__doc__)
    try:
        src = sys.stdin.read() if args[0] == "-" else open(args[0]).read()
        sys.stdout.write(run(src))
    except MuError as err:
        sys.exit(f"{args[0]}: {err}")
