"""The mu side of a solve: current.mu, the one file to work in.

    python mu/session.py stub    after serving: write current.mu
    python mu/session.py run     `make`: run the solve from current.mu
    python mu/session.py build   `make submit`: the file to submit
    python mu/session.py fold    `make solved`: file the mu solution in current.py

current.mu holds the statement as comments, a `# ---` line with
your notes under it, the Solution defs, and then the setup and
asserts, translated to mu and commented as served. current.py stays as
served; run and fold take its docstring and imports from the top and
put current.mu, transpiled, under them.
"""

import ast
import io
import os
import re
import sys
import tokenize
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from mu import MuError, Parser, fmt, transpile  # noqa: E402

CURRENT, MU, STUB, RUN = "current.py", "current.mu", ".mu_stub", ".mu_current.py"
PREV = "current.mu.prev"
CLASS = re.compile(r"^class Solution(\([^)]*\))?:", flags=re.M)
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
            args = ", ".join(a.arg for a in s.args.args)
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


def mu_def(fn):
    params = []
    for a in fn.args.args[1:]:  # past self
        t = mu_type(a.annotation)
        params.append(a.arg if t is None else f"{a.arg}: {t}")
    ret = mu_type(fn.returns)
    head = f"def {fn.name}({', '.join(params)})" + (f" -> {ret}" if ret else "")
    body = mu_lines(fn.body, 1)
    if not body or body[-1] == "":
        body.append("  pass")
    return "\n".join([head] + body)


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
    line for notes, the Solution defs with empty bodies, then the
    setup and asserts in mu. None when current.py has no Solution."""
    m = CLASS.search(py_src)
    tree = parse(py_src)
    cls = next(
        (n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "Solution"),
        None,
    )
    if cls is None or not m:
        return None
    doc = ast.get_docstring(tree) or ""
    head = [f"# {ln}".rstrip() for ln in doc.strip("\n").splitlines()]
    parts = ["\n".join(head + ["#", "# ---", ""])] if doc.strip() else []
    if cls.bases:
        parts.append(f"extends {ast.unparse(cls.bases[0])}")
    fns = [n for n in cls.body if isinstance(n, ast.FunctionDef)]
    parts.append("\n\n".join(mu_def(fn) for fn in fns))
    rest = py_src[m.end() :]
    after = re.search(r"^\S", rest, flags=re.M)
    if after:
        parts.append(mu_script(rest[after.start() :]))
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
    has a Solution class, and their titles agree."""
    mu, py = root / MU, root / CURRENT
    if not (mu.exists() and py.exists() and mu.read_text().strip()):
        return False
    py_src = py.read_text()
    return bool(CLASS.search(py_src)) and title(py_src) == title(mu.read_text(), True)


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


def spliced(py_src, mu_src, show_source=False):
    """current.py's docstring and imports, then current.mu transpiled (the
    class and the asserts). With show_source, the notes go into the
    docstring after `---` and the mu solution is quoted above the class."""
    m = CLASS.search(py_src)
    if not m:
        raise MuError("current.py has no `class Solution` to replace")
    head, code = py_src[: m.start()], transpile(mu_src)
    if show_source:
        said = notes(mu_src)
        if said:
            doc = re.match(r'\s*"""(.*?)"""', head, flags=re.S)
            if doc:
                sep = "\n" if "\n---\n" in doc.group(1) else "\n---\n"
                body = doc.group(1).rstrip("\n") + sep + said + "\n"
                head = head[: doc.start(1)] + body + head[doc.end(1) :]
        quoted = "\n".join(f"# {ln}".rstrip() for ln in solution(mu_src).splitlines())
        code = (
            "# mu source (current.mu), the candidate's solution. The Python\n"
            "# under it is the transpiler's output, and it is what ran.\n#\n"
            f"{quoted}\n\n{code}"
        )
    return head + code


# the commands


def cmd_stub(root):
    py = root / CURRENT
    if not py.exists():
        return 0
    try:
        text = stub(py.read_text())
        if text is not None:
            transpile(text)  # a stub that does not transpile would only fail at `make`
    except (MuError, SyntaxError) as err:
        print(f"mu cannot write this one ({err}), so solve it in current.py.")
        return 0
    if text is None:
        print(
            "This one has no Solution class, which mu cannot write yet, so solve it in current.py."
        )
        return 0
    mu = root / MU
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


def cmd_run(root):
    target = root / CURRENT
    if belongs(root):
        try:
            code = spliced(target.read_text(), (root / MU).read_text())
        except MuError as err:
            print(f"current.mu: {err}", file=sys.stderr)
            return 1
        target = root / RUN
        target.write_text(code)
        print("Running from current.mu.", file=sys.stderr)
    os.execv(sys.executable, [sys.executable, str(target)])


def cmd_build(root):
    """Print the file `make submit` sends: current.mu transpiled into
    .mu_current.py when current.mu holds the work, else current.py."""
    if not (belongs(root) and written(root)):
        print(CURRENT)
        return 0
    try:
        code = spliced((root / CURRENT).read_text(), (root / MU).read_text())
    except MuError as err:
        print(f"current.mu: {err}", file=sys.stderr)
        return 1
    (root / RUN).write_text(code)
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
    for name in (STUB, RUN):
        (root / name).unlink(missing_ok=True)
    print("Filed the mu solution and your notes into current.py.")
    return 0


if __name__ == "__main__":
    commands = {"stub": cmd_stub, "run": cmd_run, "build": cmd_build, "fold": cmd_fold}
    if len(sys.argv) != 2 or sys.argv[1] not in commands:
        sys.exit(__doc__)
    sys.exit(commands[sys.argv[1]](Path.cwd()))
