"""The mu side of a solve: current.mu next to current.py.

    python mu/session.py stub    after serving a drill: write its mu signature to current.mu
    python mu/session.py run     `make`: run current.py, with current.mu's
                                 solution in place of the stub once it has one
    python mu/session.py fold    `make solved`: put the mu solution into
                                 current.py for filing, and empty current.mu

The statement, the notes and the asserts stay in current.py. current.mu
counts as written once it differs from the stub served with it (kept in
.mu_stub); until then `make` runs current.py as it is.
"""

import ast
import os
import re
import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from mu import MuError, fmt, transpile  # noqa: E402

CURRENT, MU, STUB, RUN = "current.py", "current.mu", ".mu_stub", ".mu_current.py"
CLASS = re.compile(r"^class Solution(\([^)]*\))?:", flags=re.M)


# the stub


def mu_type(node):
    """A Python annotation written as a mu type."""
    if node is None:
        return None
    if isinstance(node, ast.Constant):
        return "none" if node.value is None else str(node.value)
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


class ToMu(ast.NodeTransformer):
    """Python expressions in mu spelling: range(a, b) is a..<b, True is true."""

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


def mu_expr(node):
    return ast.unparse(ToMu().visit(node))


def mu_body(stmts, ind):
    """A stub's scaffolding statements as mu lines."""
    pad, out = "  " * ind, []
    for s in stmts:
        if isinstance(s, ast.Pass):
            continue
        if isinstance(s, ast.Assign) and isinstance(s.value, ast.Lambda):
            # a helper the stub hands over, `band = lambda a, b: ...`, becomes a def
            args = ", ".join(a.arg for a in s.value.args.args)
            out += [f"{pad}def {s.targets[0].id}({args})"]
            out += [f"{pad}  {mu_expr(s.value.body)}", ""]
        elif isinstance(s, ast.For):
            it, tgt = s.iter, s.target
            enum = isinstance(it, ast.Call) and ast.unparse(it.func) == "enumerate"
            if enum:
                it = it.args[0]  # mu's `for i, x in xs` enumerates
            names = ast.unparse(tgt)
            if isinstance(tgt, ast.Tuple):
                names = ", ".join(ast.unparse(e) for e in tgt.elts)
                if not enum:
                    names = f"({names})"  # unpacking needs brackets in mu
            out.append(f"{pad}for {names} in {mu_expr(it)}")
            out += mu_body(s.body, ind + 1) or [f"{pad}  pass"]
        elif isinstance(s, (ast.If, ast.While)):
            word = "if" if isinstance(s, ast.If) else "while"
            out.append(f"{pad}{word} {mu_expr(s.test)}")
            out += mu_body(s.body, ind + 1) or [f"{pad}  pass"]
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
    body = mu_body(fn.body, 1)
    if not body or body[-1] == "":
        body.append("  pass")
    return "\n".join([head] + body)


def stub(py_src):
    """current.mu for a served current.py: its title as a comment, an
    `extends` line when Solution has a base class, and every method's
    signature with an empty body. None when there is no Solution."""
    with warnings.catch_warnings():  # a drill's ASCII art may hold "\ "
        warnings.simplefilter("ignore", SyntaxWarning)
        warnings.simplefilter("ignore", DeprecationWarning)
        tree = ast.parse(py_src)
    cls = next(
        (n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "Solution"),
        None,
    )
    if cls is None:
        return None
    doc = ast.get_docstring(tree) or ""
    title = next((ln.strip() for ln in doc.splitlines() if ln.strip()), "")
    parts = [f"# {title}"] if title else []
    if cls.bases:
        parts.append(f"extends {ast.unparse(cls.bases[0])}\n")
    fns = [n for n in cls.body if isinstance(n, ast.FunctionDef)]
    parts.append("\n\n".join(mu_def(fn) for fn in fns))
    return fmt("\n".join(parts) + "\n")


# the splice


def spliced(py_src, mu_src, show_source=False):
    """current.py with its Solution class replaced by current.mu transpiled.
    With show_source, the mu is kept above it as a comment, for the judge."""
    m = CLASS.search(py_src)
    if not m:
        raise MuError("current.py has no `class Solution` to replace")
    rest = py_src[m.end() :]
    after = re.search(r"^\S", rest, flags=re.M)
    tail = rest[after.start() :] if after else ""
    code = transpile(mu_src)
    if show_source:
        quoted = "\n".join(f"# {ln}".rstrip() for ln in mu_src.rstrip().splitlines())
        code = (
            "# mu source (current.mu), the candidate's solution. The Python\n"
            "# under it is the transpiler's output, and it is what ran.\n#\n"
            f"{quoted}\n\n{code}"
        )
    return py_src[: m.start()] + code + "\n\n" + tail


def written(root):
    """True once current.mu holds more than the stub it was served with."""
    mu = root / MU
    if not mu.exists() or not mu.read_text().strip():
        return False
    served = root / STUB
    if not served.exists():
        return True
    try:
        return fmt(mu.read_text()) != fmt(served.read_text())
    except MuError:
        return True  # an edit that does not parse yet is still an edit


# the commands


def cmd_stub(root):
    py = root / CURRENT
    if not py.exists():
        return 0
    if written(root):
        print("current.mu still holds a mu solution, so it was left alone.")
        return 0
    text = stub(py.read_text())
    if text is None or not text.startswith("# DRILL:"):
        return 0  # drills only: a leetcode submission takes the bare class
    (root / MU).write_text(text)
    (root / STUB).write_text(text)
    print("Wrote current.mu with the mu signature. Solve in either file.")
    return 0


def cmd_run(root):
    target = root / CURRENT
    if written(root):
        try:
            code = spliced(target.read_text(), (root / MU).read_text())
        except MuError as err:
            print(f"current.mu: {err}", file=sys.stderr)
            return 1
        target = root / RUN
        target.write_text(code)
        print("Running the mu solution from current.mu.", file=sys.stderr)
    os.execv(sys.executable, [sys.executable, str(target)])


def cmd_fold(root):
    if not written(root):
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
    print("Folded the mu solution into current.py for filing.")
    return 0


if __name__ == "__main__":
    commands = {"stub": cmd_stub, "run": cmd_run, "fold": cmd_fold}
    if len(sys.argv) != 2 or sys.argv[1] not in commands:
        sys.exit(__doc__)
    sys.exit(commands[sys.argv[1]](Path.cwd()))
