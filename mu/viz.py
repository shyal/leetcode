"""muviz: step through the solve in current.mu, one frame per line that
changed something.

    python mu/viz.py               step through the demo call (Enter, q)
    python mu/viz.py --all         print every frame without stopping
    python mu/viz.py file.mu       any mu file with its own script

The emitted Python runs under sys.settrace. Every line event maps back
to its mu line through the line map that `session.py debug` writes, so
a frame shows the mu source with the executed line marked, then every
variable that line changed, drawn by type: a list as a row of cells, a
grid as a table, a graph through graphviz and timg, a linked list as a
row with the pointers named, a set or dict of nodes filled in on the
graph. A subscript on the executed line, `nums[i]` or `G[u]`, marks
the cell or node it names. A memoized function reports each hit, and
the run ends with its call tree.

Only the first call into the Solution is traced: the demo line that
prints. The asserts run untraced.
"""

import argparse
import builtins
import functools
import hashlib
import io
import os
import re
import sys
import threading
import types
from collections import deque
from contextlib import redirect_stdout
from dataclasses import dataclass, field
from pathlib import Path

from rich import box
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

sys.path.insert(0, str(Path(__file__).parent))
from session import CURRENT, MU, belongs, spliced, written  # noqa: E402

from mu import MuError, Parser, transpile  # noqa: E402

RUN = ".mu_current.py"  # the traced code, written so inspect can read it
LIMIT = 1500  # frames; a longer run is cut with a note
SCALAR = (int, float, str, bool, type(None))
SUB = re.compile(r"(\w+)((?:\[[^\[\]]+\])+)")
INDEX = re.compile(r"\[([^\[\]]+)\]")
PLAIN = re.compile(r"[\w\s+\-]+")
MARK = "black on yellow"  # the cell a line writes, or its cursor
READ = "black on steel_blue1"  # a cell the line reads
ASSIGN = re.compile(r"^\s*([\w.]+(?:\[[^\[\]]+\])+)\s*(?:[-+*/|&^%]|//|<<|>>)?=(?!=)")
FILL = "green4"
MEMBER = "dark_green"


class Done(Exception):
    """Raised from the tracer once the first call into the Solution returns,
    so the rest of the script (the asserts) never runs."""


@dataclass
class Frame:
    kind: str  # call, line, return, hit, calls, note
    depth: int
    title: str
    parts: list = field(default_factory=list)  # ("text", ansi) | ("png", path)


# the state of a frame's locals, frozen so two snapshots compare


def freeze(v, seen=None):
    """A hashable, comparable copy of v: mutation shows as a difference."""
    seen = seen or set()
    if isinstance(v, SCALAR):
        return v
    node = builtins.__dict__.get("ListNode")
    tree = builtins.__dict__.get("TreeNode")
    if node and isinstance(v, node):
        return ("node", id(v))
    if tree and isinstance(v, tree):
        if id(v) in seen:
            return ("tree", "...")
        seen = seen | {id(v)}
        return ("tree", v.val, freeze(v.left, seen), freeze(v.right, seen))
    if isinstance(v, (list, tuple, deque)):
        return (type(v).__name__, tuple(freeze(x, seen) for x in v))
    if isinstance(v, dict):
        return ("dict", tuple((freeze(k, seen), freeze(x, seen)) for k, x in v.items()))
    if isinstance(v, (set, frozenset)):
        return ("set", frozenset(freeze(x, seen) for x in v))
    if hasattr(v, "__dict__") and not callable(v):
        return ("obj", freeze(vars(v), seen))
    return ("repr", repr(v))


def short(v):
    """A value for a title: a function by its name, an object by its class."""
    if callable(v):
        return getattr(v, "__name__", type(v).__name__) + "()"
    if hasattr(v, "__dict__") and type(v).__repr__ is object.__repr__:
        return type(v).__name__
    return repr(v)


def snapshot(local):
    return {
        k: freeze(v)
        for k, v in local.items()
        if k != "self" and not k.startswith("_") and not callable(v)
    }


def write_target(line):
    """The subscript a line assigns to, as text: `dp[i][j]` for
    `dp[i][j] = ...` or `count[v] += 1`; None when the line assigns none."""
    m = ASSIGN.match(line)
    return m.group(1).replace(" ", "") if m else None


def chain_text(name, chain):
    return name + "".join(f"[{t}]" for t, _ in chain).replace(" ", "")


def cursors(line, local):
    """{name: [(text, value), ...]} for every X[i] or X[i][j] on the mu
    line whose index expressions evaluate on the locals. Each entry is
    one subscript chain: `dp[i][j]` gives [("i", 1), ("j", 2)]."""
    out: dict = {}
    for name, subs in SUB.findall(line):
        if name not in local:
            continue
        chain = []
        for text in INDEX.findall(subs):
            text = text.strip()
            if ":" in text or not PLAIN.fullmatch(text):
                break
            try:
                chain.append((text, eval(text, {"__builtins__": {}}, local)))
            except Exception:
                break
        if chain:
            out.setdefault(name, []).append(chain)
    return out


# drawing one variable


def is_cell(v):
    return isinstance(v, tuple) and len(v) == 2 and all(isinstance(x, int) for x in v)


def is_row(v):
    """A flat list, tuple or deque of scalars, or of cells such as a queue
    of grid positions."""
    return isinstance(v, (list, tuple, deque)) and all(
        isinstance(x, SCALAR) or is_pair(x) for x in v
    )


def is_pair(x):
    """A short list or tuple of scalars: a cell, a (value, index) pair."""
    return (
        isinstance(x, (list, tuple))
        and 0 < len(x) <= 3
        and all(isinstance(y, SCALAR) for y in x)
    )


def is_grid(v):
    """A non-empty list of rows of scalars. The rows may be ragged: a list
    of level groups is a grid too, unless it reads as an adjacency list."""
    return (
        isinstance(v, (list, tuple))
        and bool(v)
        and all(
            isinstance(r, (list, tuple, set, frozenset))
            and all(isinstance(x, SCALAR) for x in r)
            for r in v
        )
        and not is_graph(v)
    )


def rows_of(grid):
    """The rows of a grid as lists; a set row is listed in sorted order."""
    return [
        sorted(r, key=str) if isinstance(r, (set, frozenset)) else list(r) for r in grid
    ]


def is_graph(v):
    """A dict of neighbour lists, or a ragged list of int lists whose
    entries are all indices into it."""
    if isinstance(v, dict) and v:
        if not all(isinstance(x, (list, tuple, set, dict)) for x in v.values()):
            return False
        return all(y in v for x in v.values() for y in x)  # neighbours are nodes
    if isinstance(v, list) and v and all(isinstance(x, (list, tuple)) for x in v):
        if not all(isinstance(y, int) and 0 <= y < len(v) for x in v for y in x):
            return False
        return len({len(x) for x in v}) > 1
    return False


def in_grid(cell, grid):
    return (
        is_cell(cell) and 0 <= cell[0] < len(grid) and 0 <= cell[1] < len(grid[cell[0]])
    )


def graph_nodes(G):
    G = G if isinstance(G, dict) else dict(enumerate(G))
    nodes = set(G)
    for vs in G.values():
        nodes |= set(vs)
    return G, nodes


def draw_row(name, seq, marks, styles=None, width=120):
    """A list as one row of cells; marks {index: [labels]} names cells and
    styles {index: style} colours them. A long list is drawn in chunks
    that fit the width."""
    styles = styles or {}
    cell = max([len(str(v)) for v in seq] + [len(str(len(seq)))]) + 2
    CHUNK = max(4, (width - len(name) - 6) // cell)
    t = Table(show_header=False, box=box.SIMPLE, padding=(0, 1))
    t.add_column(style="bold cyan", justify="right")
    for _ in range(min(len(seq), CHUNK)):
        t.add_column(justify="center")
    if not seq:
        t.add_column()
        t.add_row(name, Text("[]", style="dim"))
        return t
    for start in range(0, len(seq), CHUNK):
        part = range(start, min(start + CHUNK, len(seq)))
        pad = [Text("")] * (CHUNK - len(part)) if len(seq) > CHUNK else []
        idx = [Text(str(i), style="dim") for i in part]
        t.add_row(Text(""), *idx, *pad)
        if any(i in marks for i in part):
            labels = [
                Text(" ".join(marks.get(i, [])), style="bold yellow") for i in part
            ]
            t.add_row(Text(""), *labels, *pad)
        cells = [
            Text(str(seq[i]), style=styles.get(i, MARK if i in marks else ""))
            for i in part
        ]
        t.add_row(name if start == 0 else Text(""), *cells, *pad)
    return t


def draw_grid(name, grid, marks, fills=None):
    """A grid as a table. marks {(i, j): [labels]} or {(i,): [labels]}
    names cells; fills {(i, j): style} colours them."""
    fills = fills or {}
    grid = rows_of(grid)
    width = max(len(r) for r in grid)
    t = Table(box=box.SIMPLE, padding=(0, 1), title=name, title_style="bold cyan")
    t.add_column("", style="bold cyan", justify="right")
    for j in range(width):
        t.add_column(str(j), justify="right", header_style="dim")
    for i, row in enumerate(grid):
        cells = []
        for j in range(width):
            if j >= len(row):
                cells.append(Text(""))
                continue
            labels = marks.get((i, j), [])
            style = fills.get((i, j), "")
            if ((i, j) in marks and not style) or (i,) in marks:
                style = MARK
            text = f"{row[j]}" + (" " + " ".join(labels) if labels else "")
            cells.append(Text(text, style))
        head = Text(str(i), style="bold cyan")
        if (i,) in marks:
            head = Text(f"{i} {' '.join(marks[(i,)])}", style="bold yellow")
        t.add_row(head, *cells)
    return t


def draw_mapping(name, d, marks):
    """A dict or set as a two-row table: keys, then values."""
    keys = sorted(d, key=str)
    t = Table(show_header=False, box=box.SIMPLE, padding=(0, 1))
    t.add_column(style="bold cyan", justify="right")
    for _ in keys:
        t.add_column(justify="center")
    labels = [Text(" ".join(marks.get(k, [])), style="bold yellow") for k in keys]
    if marks:
        t.add_row(Text(""), *labels)
    t.add_row(name, *[Text(str(k), style=MARK if k in marks else "dim") for k in keys])
    if isinstance(d, dict):
        t.add_row(Text(""), *[Text(str(d[k])) for k in keys])
    if not keys:
        t.add_row(name, Text("{}", style="dim"))
    return t


def draw_graph(G, fills):
    """A png of G through graphviz; fills {node: (color, label)}."""
    from graphviz import Digraph, Graph

    G, nodes = graph_nodes(G)
    edges = [(u, v) for u in G for v in G[u]]
    undirected = all((v, u) in set(edges) for u, v in edges) and edges
    key = repr((sorted(edges, key=str), sorted(fills.items(), key=str)))
    path = f"/tmp/muviz_{hashlib.sha256(key.encode()).hexdigest()[:16]}"
    if os.path.exists(path + ".png"):
        return path + ".png"
    dot = Graph() if undirected else Digraph()
    dot.attr(rankdir="TB", bgcolor="transparent")
    dot.node_attr.update(
        style="filled", fillcolor="transparent", color="white", fontcolor="white"
    )
    dot.edge_attr.update(color="blue")
    for n in sorted(nodes, key=str):
        color, label = fills.get(n, ("transparent", ""))
        dot.node(
            str(n),
            label=f"{n}\\n{label}" if label else str(n),
            fillcolor=color,
            fontcolor="white" if color == "transparent" else "black",
        )
    seen = set()
    for u, v in edges:
        if undirected and (v, u) in seen:
            continue
        seen.add((u, v))
        dot.edge(str(u), str(v))
    dot.render(path, format="png", cleanup=True)
    return path + ".png"


def chain_of(node):
    vals, seen = [], set()
    while node is not None and id(node) not in seen:
        seen.add(id(node))
        vals.append(node)
        node = node.next
    return vals


def draw_linked(local, changed):
    """Every linked list among the ListNode locals, each as a row with the
    pointer variables named over the nodes they hold. A pointer inside
    another pointer's chain draws on that chain."""
    ListNode = builtins.__dict__.get("ListNode")
    if not ListNode:
        return []
    ptrs = {k: v for k, v in local.items() if isinstance(v, ListNode)}
    if not ptrs or not (set(ptrs) & changed):
        return []
    chains = sorted((chain_of(v) for v in ptrs.values()), key=len, reverse=True)
    rows = []
    for nodes in chains:
        if any(nodes[0] in done for done in rows):
            continue
        rows.append(nodes)
    out = []
    for k, nodes in enumerate(rows):
        marks: dict = {}
        for name, node in ptrs.items():
            for i, n in enumerate(nodes):
                if n is node:
                    marks.setdefault(i, []).append(name)
        out.append(
            draw_row(
                "list" if k == 0 else f"list {k + 1}", [n.val for n in nodes], marks
            )
        )
    return out


def draw_tree_text(v):
    buf = io.StringIO()
    with redirect_stdout(buf):
        builtins.__dict__["draw_tree"](v)
    return Text.from_ansi(buf.getvalue().strip("\n"))


# the tracer


class Tracer:
    def __init__(self, lines, src_lines, end=None, file=RUN):
        self.file = file
        self.lines = lines  # {python line: mu line}
        self.src = src_lines
        self.end = end or len(src_lines)  # the mu line the script starts on
        self.frames = []
        self.calls = []  # (depth, name, args, value) for the call tree
        self.depth = 0
        self.done = False
        self.state = {}  # id(frame) -> (prev snapshot, pending line)
        self.memo = set()  # names of memoized functions
        self.line = ""  # the mu line that just ran
        self.write = None  # the subscript it assigned to, as text
        self.caches = {}  # name -> its memo dict
        self.console = Console(
            file=io.StringIO(), force_terminal=True, width=min(Console().width, 120)
        )

    # the settrace protocol

    def __call__(self, frame, event, arg):
        code = frame.f_code
        if event != "call" or code.co_filename != self.file or self.done:
            return None
        if code.co_name == "<module>" or code.co_name.startswith("<"):
            return None
        if code.co_firstlineno not in self.lines:
            return None  # a pasted helper
        self.state[id(frame)] = (snapshot(frame.f_locals), None)
        if code.co_name != "run":  # the big-stack wrapper of a memo method
            args = {k: frame.f_locals[k] for k in code.co_varnames[: code.co_argcount]}
            args.pop("self", None)
            shown = self.show_args(args)  # as they arrive, before any mutation
            self.calls.append((self.depth, code.co_name, shown, None))
            self.add("call", f"{code.co_name}({shown})")
            self.depth += 1
        return self.local

    def local(self, frame, event, arg):
        if len(self.frames) >= LIMIT:
            self.cut()
            return None
        prev, pending = self.state[id(frame)]
        if event == "line":
            if pending is not None:
                self.finish(frame, pending)
            line = self.lines.get(frame.f_lineno)
            self.state[id(frame)] = (self.state[id(frame)][0], line)
        elif event == "return":
            if pending is not None:
                self.finish(frame, pending)
            self.state.pop(id(frame), None)
            if frame.f_code.co_name != "run":
                self.depth -= 1
                self.returned(frame.f_code.co_name, arg)
        return self.local

    def cut(self):
        self.done = True
        if self.frames[-1].kind != "note":
            self.add("note", f"cut after {LIMIT} frames")

    # what each event adds

    def finish(self, frame, line):
        """The frame for mu line `line`, which just ran in `frame`."""
        prev, _ = self.state[id(frame)]
        local = {
            k: v
            for k, v in frame.f_locals.items()
            if k != "self" and not k.startswith("_")
        }
        now = snapshot(local)
        self.state[id(frame)] = (now, None)
        changed = {k for k in now if k not in prev or now[k] != prev[k]}
        self.line = self.src[line - 1]
        self.write = write_target(self.line)
        marks = cursors(self.line, local)
        if not changed and not marks:
            return
        if self.src[line - 1].startswith(("def ", "extends ")):
            return  # the arguments arriving, or a grid argument wrapped
        self.add("line", f"{frame.f_code.co_name}  line {line}")
        self.source(line)
        self.variables(local, changed, marks)

    def returned(self, name, value):
        for k in range(len(self.calls) - 1, -1, -1):
            if self.calls[k][1] == name and self.calls[k][3] is None:
                self.calls[k] = self.calls[k][:3] + (value,)
                break
        self.add("return", f"{name} returns {short(value)}")
        if self.depth == 0:
            self.done = True
            self.call_tree()
            raise Done  # the demo call is over; the asserts are not wanted

    def hit(self, name, args, value):
        if self.done:
            return
        self.calls.append((self.depth, name, self.show_args(args), ("memo", value)))
        self.add("hit", f"{name}({self.show_args(args)}) = {value!r}, from the memo")
        self.memo_table(name)

    def memo_table(self, name):
        cache = self.caches.get(name)
        if cache and not self.done:
            self.render(
                draw_mapping(name, {show_key(k): v for k, v in cache.items()}, {})
            )

    def call_tree(self):
        self.add("calls", "the calls")
        root = Tree(Text("calls", style="bold"))
        stack = [root]
        for depth, name, args, value in self.calls:
            del stack[depth + 1 :]
            if isinstance(value, tuple) and value[:1] == ("memo",):
                label = Text(f"{name}({args}) = {value[1]!r}", style=MEMBER)
                label.append("  memo", style="bold yellow")
            else:
                label = Text(f"{name}({args}) = {short(value)}")
            stack.append(stack[-1].add(label))
        self.render(root)

    # rendering

    def add(self, kind, title):
        self.frames.append(Frame(kind, self.depth, title))

    def render(self, renderable):
        self.console.print(renderable)
        self.frames[-1].parts.append(("text", self.flush()))

    def flush(self):
        buf = self.console.file
        assert isinstance(buf, io.StringIO)
        self.console.file = io.StringIO()
        return buf.getvalue()

    def show_args(self, args):
        return ", ".join(f"{k}={short(v)}" for k, v in args.items())

    def source(self, line):
        lo, hi = self.window(line)
        text = Text()
        for k in range(lo, hi):
            cur = k + 1 == line
            text.append(
                f"{'>' if cur else ' '} {k + 1:>3} ",
                style="bold yellow" if cur else "dim",
            )
            text.append(self.src[k] + "\n", style="bold" if cur else "")
        self.render(text)

    def window(self, line):
        """The def block holding the mu line, or the whole solution."""
        lo = line - 1
        while lo > 0 and not self.src[lo].startswith(("def ", "extends ")):
            lo -= 1
        hi = line
        while hi < self.end - 1 and not self.src[hi].startswith(("def ", "extends ")):
            hi += 1
        while hi > lo and not self.src[hi - 1].strip():
            hi -= 1
        return lo, hi

    def variables(self, local, changed, marks):
        scalars = []
        graphs = {k: v for k, v in local.items() if is_graph(v)}
        grids = {k: v for k, v in local.items() if is_grid(v)}
        for name, chains in marks.items():
            for chain in chains:
                for text, value in chain:
                    if (
                        text in local
                        and text not in changed
                        and isinstance(value, SCALAR)
                    ):
                        scalars.append(f"{text} = {value!r}")
        for name in sorted(changed, key=lambda k: list(local).index(k)):
            v = local[name]
            if isinstance(v, SCALAR):
                scalars.append(f"{name} = {v!r}")
        if scalars:
            self.render(Text("   ".join(dict.fromkeys(scalars)), style="cyan"))
        shown = set()
        for name in list(marks) + sorted(changed, key=lambda k: list(local).index(k)):
            if name in shown or name not in local:
                continue
            shown.add(name)
            if grids and self.on_grid(local[name], grids):
                continue  # drawn onto the grid below
            self.variable(name, local[name], marks.get(name, []), graphs, local)
        for linked in draw_linked(local, changed):
            self.render(linked)
        for name, grid in grids.items():
            cell_marks, fills = self.grid_marks(name, grid, local, changed, marks)
            if name in changed or cell_marks or fills:
                self.render(draw_grid(name, grid, cell_marks, fills))
        for name, G in graphs.items():
            fills = self.fills(name, G, local, changed, marks)
            if name in changed or fills:
                self.frames[-1].parts.append(("png", draw_graph(G, fills)))

    def on_grid(self, v, grids):
        """A cell, or a set or dict of cells, that some grid in scope shows."""
        if is_cell(v):
            return any(in_grid(v, g) for g in grids.values())
        if isinstance(v, (set, frozenset, dict)) and v:
            return any(all(in_grid(c, g) for c in v) for g in grids.values())
        return False

    def grid_marks(self, gname, grid, local, changed, marks):
        """Cursor cells and coloured cells on grid gname: the subscripts on
        the line, every changed cell variable, seen-sets in green and a
        queue of cells in blue."""
        cell_marks: dict = {}
        fills: dict = {}
        for chain in marks.get(gname, []):
            vals = [val for _, val in chain]
            key = vals[0] if is_cell(vals[0]) else tuple(vals[:2])
            if len(chain) == 1 and is_cell(key) and in_grid(key, grid):
                if chain[0][0] not in cell_marks.setdefault(key, []):
                    cell_marks[key].append(chain[0][0])  # grid[c]: name the cell
            elif len(chain) == 1 and len(key) == 1 and key[0] < len(grid):
                cell_marks.setdefault(key, []).append(chain[0][0])  # grid[i]: a row
            elif is_cell(key) and in_grid(key, grid):
                write = chain_text(gname, chain) == self.write
                fills[key] = MARK if write else READ
        for name, v in local.items():
            if name == gname:
                continue
            if (
                is_cell(v)
                and in_grid(v, grid)
                and (name in changed or name in self.line)
            ):
                if name not in cell_marks.get(v, []):
                    cell_marks.setdefault(v, []).append(name)
            elif (
                isinstance(v, (set, frozenset, dict, list, deque))
                and v
                and name in changed
            ):
                if not all(in_grid(c, grid) for c in v):
                    continue
                style = "on blue" if isinstance(v, (list, deque)) else "on dark_green"
                for c in v:
                    fills[c] = style
        return cell_marks, fills

    def variable(self, name, v, chains, graphs, local):
        ListNode = builtins.__dict__.get("ListNode")
        TreeNode = builtins.__dict__.get("TreeNode")
        if isinstance(v, str) and chains:
            v = list(v)  # a string indexed on the line: a row of characters
        elif isinstance(v, SCALAR) or (ListNode and isinstance(v, ListNode)):
            return
        if TreeNode and isinstance(v, TreeNode):
            return self.render(draw_tree_text(v))
        if is_grid(v):
            return  # drawn with its marks in variables
        if is_row(v):
            marks: dict = {}
            styles: dict = {}
            for chain in chains:
                text, val = chain[0]
                if isinstance(val, int) and -len(v) <= val < len(v):
                    cell = marks.setdefault(val % len(v), [])
                    if text not in cell:
                        cell.append(text)
                    write = chain_text(name, chain[:1]) == self.write
                    if write or val % len(v) not in styles:
                        styles[val % len(v)] = MARK if write else READ
            return self.render(
                draw_row(name, list(v), marks, styles, self.console.width)
            )
        if name in graphs:
            return
        if hasattr(v, "__dict__") and vars(v):
            for attr, x in vars(v).items():
                if not attr.startswith("_") and not callable(x):
                    self.variable(f"{name}.{attr}", x, [], graphs, local)
            return
        if isinstance(v, (dict, set, frozenset)) and all(
            isinstance(k, SCALAR) or isinstance(k, tuple) for k in v
        ):
            marks = {}
            for chain in chains:
                text, val = chain[0]
                marks.setdefault(
                    val if not isinstance(val, list) else tuple(val), []
                ).append(text)
            return self.render(draw_mapping(name, v, marks))
        self.render(Text(f"{name} = {v!r}", style="cyan"))

    def fills(self, gname, G, local, changed, marks):
        """Node colours on graph gname: the cursor node gold, every node in
        a changed set or dict of nodes green with its value, a changed
        queue of nodes blue, a memo over nodes always green."""
        _, nodes = graph_nodes(G)
        fills: dict = {}
        memos = {
            n: {show_key(k): v for k, v in c.items()} for n, c in self.caches.items()
        }
        for name, v in list(local.items()) + list(memos.items()):
            if (
                name == gname
                or not isinstance(v, (dict, set, frozenset, list, deque))
                or not v
            ):
                continue
            if not all(isinstance(k, SCALAR) for k in v) or not set(v) <= nodes:
                continue
            if name in changed or name in marks or name in memos:
                color = "steelblue" if isinstance(v, (list, deque)) else FILL
                for k in v:
                    label = f"{name}={v[k]}" if isinstance(v, dict) else name
                    old = fills.get(k, ("", ""))[1]
                    fills[k] = (color, " ".join(filter(None, [old, label])))
        for chain in marks.get(gname, []):
            text, val = chain[0]
            if val in nodes:
                fills[val] = ("gold", fills.get(val, ("", ""))[1])
        return fills


def show_key(k):
    return k[0] if isinstance(k, tuple) and len(k) == 1 else k


# running the code under the tracer


def traced_cache(tracer):
    """functools.cache with the tracer told about every hit and miss."""

    def cache(fn):
        memo: dict = {}
        tracer.memo.add(fn.__name__)
        tracer.caches[fn.__name__] = memo

        @functools.wraps(fn)
        def wrapper(*args):
            if args in memo:
                names = fn.__code__.co_varnames[: fn.__code__.co_argcount]
                tracer.hit(fn.__name__, dict(zip(names, args)), memo[args])
                return memo[args]
            memo[args] = fn(*args)
            tracer.memo_table(fn.__name__)
            return memo[args]

        return wrapper

    return cache


def trace(code, lines, mu_src, path):
    """The frames of running `code`, written to `path`; lines maps its
    lines to mu lines."""
    p = Parser(mu_src)
    p.program()
    path = str(Path(path).resolve())
    Path(path).write_text(code)
    tracer = Tracer(lines, mu_src.split("\n"), p.script_line, path)
    compiled = compile(code, path, "exec")
    # a real module, so inspect finds the Solution's source for the asserts
    module = types.ModuleType("__muviz__")
    module.__file__ = path
    sys.modules["__muviz__"] = module
    env = module.__dict__
    real = functools.cache
    functools.cache = traced_cache(tracer)
    sys.settrace(tracer)
    threading.settrace(tracer)
    saved = os.dup(1), os.dup(2)
    devnull = os.open(os.devnull, os.O_WRONLY)
    os.dup2(devnull, 1)
    os.dup2(devnull, 2)
    try:
        with redirect_stdout(io.StringIO()):
            exec(compiled, env)
    except Done:
        pass
    except Exception as err:  # the run is the demo; a failing assert is not
        tracer.add("note", f"{type(err).__name__}: {err}")
    finally:
        sys.settrace(None)
        threading.settrace(None)
        functools.cache = real
        sys.modules.pop("__muviz__", None)
        os.dup2(saved[0], 1)
        os.dup2(saved[1], 2)
        os.close(saved[0])
        os.close(saved[1])
        os.close(devnull)
    return tracer.frames


def source(root, target=None):
    """(code, {python line: mu line}, mu text) for the file to step."""
    mu = root / (target or MU)
    if not mu.exists() or not mu.read_text().strip():
        raise MuError(f"{mu.name} is empty")
    text = mu.read_text()
    if target in (None, MU) and belongs(root) and written(root):
        code, lines = spliced((root / CURRENT).read_text(), text, mapped=True)
    else:
        code, lines = build(text)
    return code, lines, text


def build(mu_src, py_src=None):
    """(code, {python line: mu line}) for a mu text; with py_src, the
    Python drill whose head (docstring, imports, helper classes) it keeps."""
    if py_src is not None:
        return spliced(py_src, mu_src, mapped=True)
    code, origin = transpile(mu_src, mapped=True)
    return code, {k + 1: o for k, o in enumerate(origin) if o is not None}


def frames_of(mu_src, path, py_src=None):
    """The frames of a mu file's text, for tests."""
    code, lines = build(mu_src, py_src)
    return trace(code, lines, mu_src, path)


def play(frames, step=True, out=sys.stdout):
    styles = {"call": "bold green", "return": "bold magenta", "hit": "bold yellow"}
    console = Console(file=out, force_terminal=out.isatty())
    for k, fr in enumerate(frames):
        pad = "  " * fr.depth
        console.rule(style="bright_black")
        console.print(Text(pad + fr.title, style=styles.get(fr.kind, "bold")))
        for kind, payload in fr.parts:
            if kind == "text":
                out.write(payload)
            elif out.isatty():
                out.flush()
                os.system(f"timg -g50x25 {payload}")
            else:
                out.write(f"[graph {payload}]\n")
        if step and k + 1 < len(frames):
            try:
                if input().strip().lower() == "q":
                    return
            except EOFError:
                return


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("file", nargs="?", help="a mu file; current.mu by default")
    ap.add_argument("--all", action="store_true", help="print every frame, no stepping")
    a = ap.parse_args(argv)
    root = Path(__file__).resolve().parent.parent
    try:
        code, lines, text = source(root, a.file)
    except MuError as err:
        print(f"muviz: {err}", file=sys.stderr)
        return 1
    frames = trace(code, lines, text, root / RUN)
    if not frames:
        print("muviz: the script never calls the Solution", file=sys.stderr)
        return 1
    play(frames, step=not a.all and sys.stdin.isatty())
    return 0


if __name__ == "__main__":
    sys.exit(main())
