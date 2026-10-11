"""The mu side of a solve: current.mu, the one file to work in.

    python mu/session.py stub    after serving: write current.mu
    python mu/session.py run [file.mu] [--color|--no-color]
                                 `make`: run the solve from current.mu, in place;
                                 or any mu file on its own
    python mu/session.py build   `make submit`: the file to submit
    python mu/session.py fold    `make solved`: file the mu solution in current.py
    python mu/session.py debug [file.mu]   VS Code: write .mu_current.py and its line map

current.mu holds the statement as comments, a `# ---` line with
your notes under it, the solve (the classes and defs of current.py:
`class Solution`, a design problem's class, a given helper), and then
the setup and asserts, translated to mu and commented as served.
current.py stays as served; run and fold take its docstring and imports
from the top and put current.mu, transpiled, under them. run writes no
file: the Python is compiled under current.mu's name with each statement
at its mu line, so a failed assert or an exception reports the line in
current.mu. The harness helpers pasted in by the transpiler are compiled
apart, as <mu helpers>. While current.mu is still the stub as served, run
runs current.py, so a drill mu has no word for is solved there.
"""

import ast
import io
import json
import linecache
import os
import re
import sys
import tokenize
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from mu import VERSION, MuError, Parser, fmt, transpile  # noqa: E402

CURRENT, MU, STUB, RUN = "current.py", "current.mu", ".mu_stub", ".mu_current.py"
MAP = ".mu_current.map.json"
HELPERS = "<mu helpers>"  # the file name of the pasted helpers' frames
PREV = "current.mu.prev"
SOLVE = (ast.ClassDef, ast.FunctionDef)  # the top-level nodes a solve is made of
# a commented line the asserts need: an assert, `name = ...`, `name += ...`
# or a `sol.method(...)` call (utils/tests/test_reference_solutions.py SETUP)
SETUP = r"(?:assert |[\w.\[\]]+ (?:[-+*/]|//)?= |sol\.\w+\()"


def parse(src):
    with warnings.catch_warnings():  # a drill's ASCII art may hold "\ "
        warnings.simplefilter("ignore", SyntaxWarning)
        warnings.simplefilter("ignore", DeprecationWarning)
        return ast.parse(src)


# Python to mu


def mu_type(node):
    """A Python annotation written as a mu type."""
    if node is None:
        return None
    if isinstance(node, ast.Constant):
        if isinstance(node.value, str):  # a quoted annotation: 'Optional[Node]'
            return mu_type(ast.parse(node.value, mode="eval").body)
        return "none" if node.value is None else str(node.value)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
        sides = [node.left, node.right]
        rest = [
            n for n in sides if not (isinstance(n, ast.Constant) and n.value is None)
        ]
        if len(rest) == 1:  # TreeNode | None
            return f"{mu_type(rest[0])}?"
    if isinstance(node, ast.Name):
        return {"None": "none"}.get(node.id, node.id)
    if isinstance(node, ast.Subscript):
        head = ast.unparse(node.value).split(".")[-1].lower()
        args = node.slice.elts if isinstance(node.slice, ast.Tuple) else [node.slice]
        if head == "list":
            return f"[{mu_type(args[0])}]"
        if head == "dict":
            return f"{{{mu_type(args[0])}: {mu_type(args[1])}}}"
        if head == "set":
            return f"{{{mu_type(args[0])}}}"
        if head == "tuple":
            return "(" + ", ".join(mu_type(a) for a in args) + ")"
        if head == "optional":
            return f"{mu_type(args[0])}?"
        if head == "callable":
            params = [mu_type(a) for a in args[0].elts]
            takes = params[0] if len(params) == 1 else "(" + ", ".join(params) + ")"
            return f"{takes} -> {mu_type(args[1])}"
    return ast.unparse(node)


def loop_head(target, it):
    """The target and iterable of a Python loop, in mu: `for i, x in xs`
    enumerates, so a Python `enumerate(xs)` drops the call, and plain
    unpacking gets brackets, `for (a, b) in pairs`."""
    enum = isinstance(it, ast.Call) and ast.unparse(it.func) == "enumerate"
    enum = enum and len(it.args) == 1 and not it.keywords
    if not isinstance(target, ast.Tuple):
        return ast.unparse(target), it
    names = ", ".join(ast.unparse(e) for e in target.elts)
    return (names, it.args[0]) if enum else (f"({names})", it)


class ToMu(ast.NodeTransformer):
    """Python expressions in mu spelling: range(a, b) is a..<b, True is
    true, lambda x: e is x -> e, and comprehension targets as mu loops."""

    def visit_Call(self, node):
        self.generic_visit(node)
        if (
            isinstance(node.func, ast.Name)
            and node.func.id == "range"
            and not node.keywords
        ):
            args = [ast.unparse(a) for a in node.args]
            if len(args) == 1:
                return ast.Name(id=f"0..<{args[0]}")
            if len(args) == 2:
                return ast.Name(id=f"{args[0]}..<{args[1]}")
        return node

    def visit_Constant(self, node):
        if node.value is True or node.value is False or node.value is None:
            return ast.Name(id=str(node.value).lower())
        return node

    def visit_Lambda(self, node):
        args = [a.arg for a in node.args.args]
        if len(args) != 1:
            raise MuError(f"no mu form for a lambda of {len(args)} arguments")
        return ast.Name(id=f"{args[0]} -> {mu_expr(node.body)}")

    def visit_comprehension(self, node):
        self.generic_visit(node)
        names, it = loop_head(node.target, node.iter)
        node.target, node.iter = ast.Name(id=names), it
        return node


def mu_expr(node):
    return ast.unparse(ToMu().visit(node))


def bare(node):
    """An expression in mu; a tuple without its brackets: `a, b = f(x)`."""
    if isinstance(node, ast.Tuple) and node.elts:
        return ", ".join(mu_expr(e) for e in node.elts)
    return mu_expr(node)


def mu_lines(stmts, ind):
    """Python statements as mu lines."""
    pad, out = "  " * ind, []
    for s in stmts:
        if isinstance(s, ast.Pass):
            continue
        if isinstance(s, ast.Assign) and isinstance(s.value, ast.Lambda):
            # a helper handed over as `band = lambda a, b: ...` becomes a def
            args = ", ".join(a.arg for a in s.value.args.args)
            out += [f"{pad}def {s.targets[0].id}({args})"]
            out += [f"{pad}  {mu_expr(s.value.body)}", ""]
        elif isinstance(s, ast.FunctionDef):
            args = ", ".join(a.arg for a in plain_params(s))
            out.append(f"{pad}def {s.name}({args})")
            out += mu_lines(s.body, ind + 1) or [f"{pad}  pass"]
            out.append("")
        elif isinstance(s, ast.For):
            names, it = loop_head(s.target, s.iter)
            out.append(f"{pad}for {names} in {mu_expr(it)}")
            out += mu_lines(s.body, ind + 1) or [f"{pad}  pass"]
        elif isinstance(s, (ast.If, ast.While)):
            word = "if" if isinstance(s, ast.If) else "while"
            out.append(f"{pad}{word} {mu_expr(s.test)}")
            out += mu_lines(s.body, ind + 1) or [f"{pad}  pass"]
        elif isinstance(s, ast.Return):
            out.append(
                pad + ("return" if s.value is None else f"return {bare(s.value)}")
            )
        elif isinstance(s, ast.Assign):
            lhs = " = ".join(bare(t) for t in s.targets)
            out.append(f"{pad}{lhs} = {bare(s.value)}")
        else:
            out.append(pad + mu_expr(s))
    return out


def body_comments(fn, py_lines):
    """The whole-line comments inside a def, as mu body lines. The syntax
    tree drops them, and a drill's mnemonic is one of them."""
    span = py_lines[fn.lineno : fn.end_lineno]
    return ["  " + ln.strip() for ln in span if ln.strip().startswith("#")]


def plain_params(fn):
    """The parameters of a def mu can write: positional, no default, no
    *args or **kwargs, no decorator. A method's self is dropped: mu adds it."""
    a = fn.args
    if a.defaults or a.kwonlyargs or a.vararg or a.kwarg or a.posonlyargs:
        raise MuError(f"{fn.name} has a parameter mu cannot write")
    if fn.decorator_list:
        raise MuError(f"{fn.name} has a decorator")
    args = a.args
    return args[1:] if args and args[0].arg == "self" else args


def mu_def(fn, comments=()):
    """A Python def as a mu def."""
    params = []
    for a in plain_params(fn):
        t = mu_type(a.annotation)
        params.append(a.arg if t is None else f"{a.arg}: {t}")
    ret = mu_type(fn.returns)
    head = f"def {fn.name}({', '.join(params)})" + (f" -> {ret}" if ret else "")
    body = mu_lines(fn.body, 1)
    if not body or body[-1] == "":
        body.append("  pass")
    return "\n".join([head] + list(comments) + body)


def mu_class(cls, py_lines):
    """A Python class as a mu class: `class Name extends Base`, its
    methods as defs, its attributes as assignments."""
    above = [f"@{ast.unparse(d)}" for d in cls.decorator_list]
    head = f"class {cls.name}"
    if cls.bases:
        head += " extends " + ", ".join(ast.unparse(b) for b in cls.bases)
    body = []
    for n in cls.body:
        if isinstance(n, ast.FunctionDef):
            lines = mu_def(n, body_comments(n, py_lines)).split("\n")
            body += [f"  {ln}" if ln else "" for ln in lines] + [""]
        elif isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant):
            continue  # a docstring
        else:
            body += mu_lines([n], 1)
    while body and body[-1] == "":
        body.pop()
    return "\n".join(above + [head] + (body or ["  pass"]))


def placeholder(n):
    """A class or def served to be written: its body is only `pass`."""
    body = [
        s
        for s in n.body
        if not (isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant))
    ]
    return len(body) == 1 and isinstance(body[0], ast.Pass)


def solve_nodes(tree):
    """The top-level nodes of current.py that are the solve, in order: `class
    Solution`, the `pass`-bodied classes and defs just above it (served to
    be written; a class with a body above it is given, and stays Python),
    and the classes and defs that follow it. Without a Solution class, the
    first run of classes and defs (a design problem's class). [] when there
    is none."""
    nodes = tree.body
    sol = next(
        (
            k
            for k, n in enumerate(nodes)
            if isinstance(n, ast.ClassDef) and n.name == "Solution"
        ),
        None,
    )
    if sol is None:
        i = next((k for k, n in enumerate(nodes) if isinstance(n, SOLVE)), None)
        if i is None:
            return []
    else:
        i = sol
        while i > 0 and isinstance(nodes[i - 1], SOLVE) and placeholder(nodes[i - 1]):
            i -= 1
    j = i if sol is None else sol
    while j + 1 < len(nodes) and isinstance(nodes[j + 1], SOLVE):
        j += 1
    return nodes[i : j + 1]


def solve_span(py_src):
    """(start, end), character offsets in current.py: from the first line of
    the solve (a decorator counts) to the first line at column 0 after it,
    where the setup and asserts begin. None when current.py has no solve."""
    nodes = solve_nodes(parse(py_src))
    if not nodes:
        return None
    lines = py_src.splitlines(keepends=True)
    offsets = [0]
    for ln in lines:
        offsets.append(offsets[-1] + len(ln))
    first = min([nodes[0].lineno] + [d.lineno for d in nodes[0].decorator_list])
    k = nodes[-1].end_lineno  # 0-based index of the line after the solve
    while k < len(lines) and (not lines[k].strip() or lines[k][0] in " \t"):
        k += 1
    return offsets[first - 1], offsets[k]


def brackets(line):
    """Opened minus closed brackets on a line, outside strings and comments."""
    code = re.sub(r"'[^']*'|\"[^\"]*\"", "", line.split("  #")[0])
    return sum(code.count(c) for c in "([{") - sum(code.count(c) for c in ")]}")


def turned_on(lines):
    """The lines with every commented setup line and assert turned on, and
    the commented lines that continue one left open (`assert f(x) == [`)."""
    out, depth = [], 0
    for line in lines:
        if depth > 0 and line.startswith("#"):
            line = line[2:] if line.startswith("# ") else line[1:]
        elif re.match(rf"# {SETUP}", line):
            line = line[2:]
        elif not re.match(SETUP, line):
            out.append(line)
            continue
        depth = max(0, depth + brackets(line))
        out.append(line)
    return out


def mu_script(tail):
    """The drill's setup and asserts, after its Solution class, in mu. A
    line that was commented out stays commented; other comments and a
    statement's trailing comment (`print(...)  # 3`) are kept."""
    lines = tail.split("\n")
    on = turned_on(lines)
    commented = {i + 1 for i, (a, b) in enumerate(zip(lines, on)) if a != b}
    source = "\n".join(on)
    trailing = {}
    for tok in tokenize.generate_tokens(io.StringIO(source).readline):
        if (
            tok.type == tokenize.COMMENT
            and on[tok.start[0] - 1][: tok.start[1]].strip()
        ):
            trailing[tok.start[0]] = tok.string
    out, prev = [], 0
    for s in parse(source).body:
        for n in range(prev + 1, s.lineno):
            out.append(on[n - 1] if on[n - 1].lstrip().startswith("#") else "")
        mu = mu_lines([s], 0)
        while mu and mu[-1] == "":
            mu.pop()
        if s.end_lineno in trailing and mu:
            mu[-1] += "  " + trailing[s.end_lineno]
        if s.lineno in commented:
            mu = [f"# {m}" if m else "#" for m in mu]
        out += mu + ([""] if isinstance(s, ast.FunctionDef) else [])
        prev = s.end_lineno
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip("\n")


def stub(py_src):
    """current.mu for a served drill or problem: the statement as comments, a `# ---`
    line for notes, the classes and defs of the solve with their bodies as
    served (empty, mostly), then the setup and asserts in mu. None when
    current.py has no class or def."""
    tree = parse(py_src)
    nodes = solve_nodes(tree)
    if not nodes:
        return None
    doc = ast.get_docstring(tree) or ""
    head = [f"# {ln}".rstrip() for ln in doc.strip("\n").splitlines()]
    parts = ["\n".join(head + ["#", "# ---", ""])] if doc.strip() else []
    py_lines = py_src.splitlines()
    for n in nodes:
        if isinstance(n, ast.ClassDef):
            parts.append(mu_class(n, py_lines))
        else:
            parts.append(mu_def(n, body_comments(n, py_lines)))
    _, end = solve_span(py_src)
    if end < len(py_src):
        parts.append(mu_script(py_src[end:]))
    return fmt("\n\n".join(parts) + "\n")


# current.py and current.mu together


def title(text, comment=False):
    """The first line of a statement: `DRILL: Count Cells`."""
    if comment:
        first = text.split("\n", 1)[0]
        return first[1:].strip() if first.startswith("#") else ""
    try:
        doc = ast.get_docstring(parse(text)) or ""
    except SyntaxError:
        return ""
    return next((ln.strip() for ln in doc.splitlines() if ln.strip()), "")


def belongs(root):
    """current.mu is the solve in current.py: it is not empty, current.py
    has a solve (a class or a def), and their titles agree."""
    mu, py = root / MU, root / CURRENT
    if not (mu.exists() and py.exists() and mu.read_text().strip()):
        return False
    py_src = py.read_text()
    try:
        span = solve_span(py_src)
    except SyntaxError:
        return False
    return span is not None and title(py_src) == title(mu.read_text(), True)


def written(root):
    """current.mu holds more than the stub it was served with."""
    mu, served = root / MU, root / STUB
    if not mu.exists() or not mu.read_text().strip():
        return False
    if not served.exists():
        return True
    try:
        return fmt(mu.read_text()) != fmt(served.read_text())
    except MuError:
        return True  # an edit that does not parse yet is still an edit


def notes(mu_src):
    """The comment lines under `# ---` in current.mu's statement block."""
    out, on = [], False
    for line in mu_src.split("\n"):
        if not line.startswith("#"):
            if line.strip():
                break
            continue
        if line.rstrip() == "# ---":
            on = True
        elif on:
            out.append(line[2:] if line.startswith("# ") else line[1:])
    return "\n".join(out).strip()


def solution(mu_src):
    """current.mu between the statement block and the script: the part
    the candidate wrote, quoted for the judge."""
    p = Parser(mu_src)
    p.program()
    lines = mu_src.split("\n")
    end = (p.script_line or len(lines) + 1) - 1
    start = 0
    while start < end and (not lines[start].strip() or lines[start].startswith("#")):
        start += 1
    return "\n".join(lines[start:end]).strip("\n")


def spliced(py_src, mu_src, show_source=False, mapped=False):
    """current.py's docstring and imports, then current.mu transpiled (the
    solve and the asserts). With show_source, the notes go into the
    docstring after `---` and the mu solution is quoted above the solve,
    under a `# mu <version>` line. With mapped, also {python line: mu line},
    both 1-based, for every line that came from current.mu."""
    span = solve_span(py_src)
    if span is None:
        raise MuError("current.py has no class or def to replace")
    head = py_src[: span[0]]
    code, origin = transpile(mu_src, mapped=True)
    if show_source:
        said = notes(mu_src)
        if said:
            doc = re.match(r'\s*"""(.*?)"""', head, flags=re.S)
            if doc:
                sep = "\n" if "\n---\n" in doc.group(1) else "\n---\n"
                body = doc.group(1).rstrip("\n") + sep + said + "\n"
                head = head[: doc.start(1)] + body + head[doc.end(1) :]
        quoted = "\n".join(f"# {ln}".rstrip() for ln in solution(mu_src).splitlines())
        code = f"# mu {VERSION}\n{quoted}\n\n{code}"
    out = head + code
    if not mapped:
        return out
    skip = out.count("\n") - len(origin)  # lines above the transpiled code
    lines = {skip + k + 1: o for k, o in enumerate(origin) if o is not None}
    return out, lines


# the commands


def cmd_stub(root):
    py = root / CURRENT
    if not py.exists() or not py.read_text().strip():
        return 0
    mu = root / MU
    try:
        text = stub(py.read_text())
        if text is not None:
            transpile(text)  # a stub that does not transpile would only fail at `make`
    except (MuError, SyntaxError) as err:
        print(f"mu cannot write this one ({err}), so solve it in current.py.")
        return 0
    if text is None:
        print("This one has no class or def, so solve it in current.py.")
        return 0
    if written(root):
        if belongs(root):
            print("current.mu already holds work on this one, so it was left alone.")
            return 0
        (root / PREV).write_text(mu.read_text())
        print(f"current.mu held work on another solve; it was moved to {PREV}.")
    mu.write_text(text)
    (root / STUB).write_text(text)
    print("Wrote current.mu: the statement, the signature and the asserts, in mu.")
    return 0


OPS = {
    ast.Eq: "==",
    ast.NotEq: "!=",
    ast.Lt: "<",
    ast.LtE: "<=",
    ast.Gt: ">",
    ast.GtE: ">=",
    ast.Is: "is",
    ast.IsNot: "is not",
    ast.In: "in",
    ast.NotIn: "not in",
}


def with_messages(tree):
    """Every bare `assert L op R` in tree reports both sides. Each side is
    bound as it is evaluated, `(_l := L) op (_r := R)`, so the message
    shows the values the assert saw and a side with side effects is not
    run a second time. Line numbers are kept."""
    for node in ast.walk(tree):
        test = node.test if isinstance(node, ast.Assert) and node.msg is None else None
        if not (isinstance(test, ast.Compare) and len(test.ops) == 1):
            continue
        op = OPS[type(test.ops[0])]
        test.left = ast.NamedExpr(ast.Name("_l", ast.Store()), test.left)
        test.comparators[0] = ast.NamedExpr(
            ast.Name("_r", ast.Store()), test.comparators[0]
        )
        msg = "left : {_l!r}\\nright: {_r!r}" + (
            "" if op == "==" else f"\\nop   : {op}"
        )
        node.msg = ast.parse(f'f"{msg}"', mode="eval").body
        ast.copy_location(node.msg, node)
    return ast.fix_missing_locations(tree)


def compiled(src, filename):
    """src compiled as filename, its asserts through `with_messages`."""
    return compile(with_messages(ast.parse(src, filename)), filename, "exec")


def mu_line(origin, k):
    """The mu line behind Python line k (1-based). A line with no origin,
    such as `class Solution:` or a blank, takes the nearest mu line before
    it, or after it when none comes before."""
    before = [o for o in origin[:k] if o is not None]
    if before:
        return before[-1]
    after = [o for o in origin[k:] if o is not None]
    return after[0] if after else 1


def relocated(tree, origin):
    """tree with every node moved from its Python line to the mu line it
    came from, so the code it compiles to reports current.mu's lines."""
    for node in ast.walk(tree):
        if not hasattr(node, "lineno"):
            continue
        node.lineno = mu_line(origin, node.lineno)
        if getattr(node, "end_lineno", None) is not None:
            node.end_lineno = max(node.lineno, mu_line(origin, node.end_lineno))
    return tree


def mu_code(mu_src, filename):
    """A mu file as two code objects, (helpers, program). The program is
    the file's own statements, the class and the script, each at its mu
    line under filename. The helpers are the imports and harness functions
    the transpiler pastes in, under the name HELPERS; their source is kept
    in linecache so a traceback through one still shows the line."""
    code, origin = transpile(mu_src, mapped=True)
    try:
        tree = ast.parse(code)
    except SyntaxError as err:
        raise MuError(f"line {mu_line(origin, err.lineno or 1)}: {err.msg}") from None
    own = [
        s
        for s in tree.body
        if isinstance(s, ast.ClassDef) or origin[s.lineno - 1] is not None
    ]
    helpers = [s for s in tree.body if s not in own]
    linecache.cache[HELPERS] = (len(code), None, code.splitlines(True), HELPERS)
    program = relocated(with_messages(ast.Module(own, type_ignores=[])), origin)
    return (
        compile(ast.Module(helpers, type_ignores=[]), HELPERS, "exec"),
        compile(program, filename, "exec"),
    )


FRAME = re.compile(r'^  File "(.*?)", line (\d+), in (.*)$')
RAISED = re.compile(r"^([A-Z]\w*(?:\.\w+)*)(: .*)?$")
BOLD, DIM, RED, GREEN, YELLOW, MAGENTA, RESET = (
    "\033[1m",
    "\033[2m",
    "\033[31m",
    "\033[32m",
    "\033[33m",
    "\033[35m",
    "\033[0m",
)


def painted(text):
    """A traceback with colour: each frame's file dim and its line number
    yellow, the source line bold, the exception red, and in an assert's
    message the left side (what the code gave) red and the right side
    (what the assert wanted) green. Paths under the working directory are
    shortened to relative ones either way."""
    out = []
    for line in text.rstrip("\n").split("\n"):
        m = FRAME.match(line)
        if m:
            file, n, fn = m.groups()
            if os.path.isabs(file) and file.startswith(os.getcwd() + os.sep):
                file = os.path.relpath(file)
            line = f'  File "{DIM}{file}{RESET}", line {YELLOW}{n}{RESET}, in {MAGENTA}{fn}{RESET}'
        elif line.startswith("    "):
            line = f"{BOLD}{line}{RESET}"
        elif RAISED.match(line):
            name, rest = RAISED.match(line).groups()
            line = f"{RED}{BOLD}{name}{RESET}{rest or ''}"
            line = line.replace(": left : ", f": {RED}left :{RESET} ", 1)
        elif line.startswith("right: "):
            line = f"{GREEN}right:{RESET}" + line[6:]
        out.append(line)
    return "\n".join(out) + "\n"


def run(codes, target, color=False):
    """Run the code objects in order, like `python target`: in a fresh
    `__main__` module whose file is target, so `inspect` (the harness's
    uses, avoids and folds) reads the class from there and not from this
    script. On an uncaught exception the traceback starts at the script's
    own frame, through `painted` when color is on, and the exit status
    is 1."""
    import traceback
    import types

    sys.argv = [str(target)]
    main = types.ModuleType("__main__")
    main.__file__ = str(target)
    sys.modules["__main__"] = main
    try:
        for code in codes:
            exec(code, main.__dict__)
    except SystemExit:
        raise
    except BaseException as err:  # noqa: BLE001
        text = "".join(
            traceback.format_exception(type(err), err, err.__traceback__.tb_next)
        )
        sys.stderr.write(painted(text) if color else text)
        return 1
    return 0


def run_file(target, color=False):
    """Run target as a script, with its asserts compiled by `compiled`."""
    return run([compiled(target.read_text(), str(target))], target, color)


def cmd_run(root, *args):
    """`make`: run current.mu in place when it is the solve and holds more
    than the stub, else current.py. current.py's head, the docstring and
    imports above its solve, runs first under its own name, then
    current.mu's code under its own. No file is written. `run FILE.mu`
    runs any mu file on its own, with no current.py head. The traceback is
    coloured on a terminal, or with --color; --no-color turns it off."""
    color = sys.stderr.isatty()
    files = []
    for a in args:
        if a == "--color":
            color = True
        elif a == "--no-color":
            color = False
        else:
            files.append(a)
    if len(files) > 1:
        sys.exit(__doc__)
    if files and not (files[0] == MU and belongs(root)):
        mu = root / files[0]
        try:
            codes = mu_code(mu.read_text(), str(mu))
        except MuError as err:
            print(f"{files[0]}: {err}", file=sys.stderr)
            return 1
        return run(list(codes), mu, color)
    py = root / CURRENT
    if not (belongs(root) and written(root)):
        return run_file(py, color)
    py_src = py.read_text()
    head = py_src[: solve_span(py_src)[0]]
    try:
        helpers, program = mu_code((root / MU).read_text(), str(root / MU))
    except MuError as err:
        print(f"current.mu: {err}", file=sys.stderr)
        return 1
    print("Running from current.mu.", file=sys.stderr)
    return run([compile(head, str(py), "exec"), helpers, program], root / MU, color)


def cmd_build(root):
    """Print the file `make submit` sends: current.mu transpiled into
    .mu_current.py when current.mu holds the work, else current.py. The
    mu solution is quoted above the class, and leetcode gets it too."""
    if not (belongs(root) and written(root)):
        print(CURRENT)
        return 0
    try:
        code = spliced(
            (root / CURRENT).read_text(), (root / MU).read_text(), show_source=True
        )
    except MuError as err:
        print(f"current.mu: {err}", file=sys.stderr)
        return 1
    (root / RUN).write_text(code)
    print(RUN)
    return 0


def cmd_debug(root, target=None):
    """Write .mu_current.py for the debugger, with .mu_current.map.json
    beside it: {"file": <the mu file>, "lines": {python line: mu line}}.
    current.mu is spliced into current.py when it is the live solve; any
    other mu file, or current.mu once the solve is filed, is transpiled on
    its own. Prints the file to debug: .mu_current.py, or current.py when
    there is no mu to debug."""
    mu = root / (target or MU)
    current = target in (None, MU) and belongs(root)
    live = current and written(root)
    untouched = current and not live  # the stub as served: debug current.py
    if untouched or not (mu.exists() and mu.read_text().strip()):
        (root / MAP).unlink(missing_ok=True)
        print(CURRENT)
        return 0
    try:
        if live:
            code, lines = spliced(
                (root / CURRENT).read_text(),
                mu.read_text(),
                show_source=True,
                mapped=True,
            )
        else:
            code, origin = transpile(mu.read_text(), mapped=True)
            lines = {k + 1: o for k, o in enumerate(origin) if o is not None}
    except MuError as err:
        print(f"{mu.name}: {err}", file=sys.stderr)
        return 1
    (root / RUN).write_text(code)
    (root / MAP).write_text(json.dumps({"file": target or MU, "lines": lines}))
    print(RUN)
    return 0


def cmd_fold(root):
    if not belongs(root) or not written(root):
        return 0
    py = root / CURRENT
    try:
        code = spliced(py.read_text(), (root / MU).read_text(), show_source=True)
    except MuError as err:
        print(f"current.mu: {err}", file=sys.stderr)
        return 1
    py.write_text(code)
    (root / MU).write_text("")
    for name in (STUB, RUN, MAP):
        (root / name).unlink(missing_ok=True)
    print("Filed the mu solution and your notes into current.py.")
    return 0


if __name__ == "__main__":
    commands = {
        "stub": cmd_stub,
        "run": cmd_run,
        "build": cmd_build,
        "fold": cmd_fold,
        "debug": cmd_debug,
    }
    argv = sys.argv[1:]
    if argv[:1] == ["debug"] and len(argv) == 2:
        sys.exit(cmd_debug(Path.cwd(), argv[1]))
    if argv[:1] == ["run"]:
        sys.exit(cmd_run(Path.cwd(), *argv[1:]))
    if len(argv) != 1 or argv[0] not in commands:
        sys.exit(__doc__)
    sys.exit(commands[argv[0]](Path.cwd()))
