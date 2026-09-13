"""Derive a candidate stub from a validated solution.

The prepare cache stores the full solution that passed its own asserts; the
stub written to `current.py` is derived from it here. The transform is
line-based and driven by `ast`, so the docstring, spacing and comments of the
original survive byte-for-byte - only method bodies and asserts are touched.
"""

import ast


def _end(node):
    """Last line of an ast node. The parser always fills end_lineno in; the
    stub type says Optional, so this pins it to int."""
    assert node.end_lineno is not None
    return node.end_lineno


# injected by sitecustomize; if a generator redefines one anyway, leave it
# working rather than gutting it and breaking the file.
HELPER_CLASSES = {"TreeNode", "ListNode", "GraphNode", "Node"}


# modules whose contents sitecustomize already injects; importing from them
# is always redundant in a solve file.
INJECTED_MODULES = {
    "typing",
    "collections",
    "functools",
    "itertools",
    "math",
    "heapq",
    "bisect",
    "string",
}


def _indent_of(line):
    return line[: len(line) - len(line.lstrip())]


def sanitize(code):
    """Remove top-level statements a generator emits out of habit that the
    sitecustomize environment makes redundant: imports from injected modules
    and redefinitions of the helper classes. Returns the cleaned source."""
    tree = ast.parse(code)
    drop: set[int] = set()
    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and node.module in INJECTED_MODULES:
            drop.update(range(node.lineno, _end(node) + 1))
        elif isinstance(node, ast.Import) and all(
            a.name in INJECTED_MODULES for a in node.names
        ):
            drop.update(range(node.lineno, _end(node) + 1))
        elif isinstance(node, ast.ClassDef) and node.name in HELPER_CLASSES:
            drop.update(range(node.lineno, _end(node) + 1))
    if drop:
        src = code.splitlines()
        out = [l for i, l in enumerate(src, start=1) if i not in drop]
        # collapse the blank run left where a block was removed
        text = "\n".join(out)
        while "\n\n\n\n" in text:
            text = text.replace("\n\n\n\n", "\n\n\n")
        code = text.lstrip("\n").rstrip() + "\n"
    return hoist_builders(code)


# builder -> the variable name used when the callee's parameter name is unknown
BUILDERS = {"build_tree": "root", "build_linked_list": "head"}


def _builder_default(node):
    """The fallback variable name when `node` calls a builder, else None."""
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        return BUILDERS.get(node.func.id)
    return None


def _is_builder_call(node):
    return _builder_default(node) is not None


def _is_bare_print(stmt):
    """`print(x)` / `draw_tree(x)` of a plain name: shows a value, tests nothing."""
    if not (isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call)):
        return False
    call = stmt.value
    if not (isinstance(call.func, ast.Name) and len(call.args) == 1):
        return False
    return isinstance(call.args[0], ast.Name) and not call.keywords


def is_demo(stmt):
    """The first-example call: a print or draw that is not a bare `print(x)`."""
    if not (isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call)):
        return False
    fn = stmt.value.func
    name = fn.id if isinstance(fn, ast.Name) else getattr(fn, "attr", "")
    shows = name in {"print", "tabulate", "rich_print"} or name.startswith("draw_")
    return shows and not _is_bare_print(stmt)


def _param_names(tree, call):
    """Parameter names of the method or constructor `call` invokes, minus self.
    None when the callee is not defined in the file."""
    fn = call.func
    for cls in tree.body:
        if not isinstance(cls, ast.ClassDef):
            continue
        for member in cls.body:
            if not isinstance(member, ast.FunctionDef):
                continue
            hit = (isinstance(fn, ast.Attribute) and member.name == fn.attr) or (
                isinstance(fn, ast.Name)
                and fn.id == cls.name
                and member.name == "__init__"
            )
            if hit:
                return [a.arg for a in member.args.args[1:]]
    return None


def _splice(lines, node, text):
    """Replace the source of `node` (0-based lines list) with `text`."""
    r0, c0 = node.lineno - 1, node.col_offset
    r1, c1 = _end(node) - 1, node.end_col_offset
    lines[r0 : r1 + 1] = [lines[r0][:c0] + text + lines[r1][c1:]]


def hoist_builders(code):
    """A tree or linked list passed inline to the first-example call is built
    into a variable named after the parameter, printed on its own line (the
    harness draws it), then passed. Statements after the demo are untouched."""
    tree = ast.parse(code)
    demo = next((s for s in tree.body if is_demo(s)), None)
    if demo is None:
        return code
    lines = code.splitlines()
    taken = {
        t.id
        for s in tree.body
        if isinstance(s, ast.Assign) and s.lineno <= demo.lineno
        for t in s.targets
        if isinstance(t, ast.Name)
    }
    printed = {
        s.value.args[0].id
        for s in tree.body
        if s.lineno <= demo.lineno and _is_bare_print(s)
    }
    edits = []  # (stmt, [(call, name)], print_only_names)
    for stmt in tree.body:
        if stmt.lineno > demo.lineno or not isinstance(stmt, (ast.Expr, ast.Assign)):
            continue
        hoists = []
        for call in ast.walk(stmt):
            if not isinstance(call, ast.Call) or _is_builder_call(call):
                continue
            params = _param_names(tree, call)
            for i, arg in enumerate(call.args):
                default = _builder_default(arg)
                if default is not None:
                    base = params[i] if params and i < len(params) else None
                    hoists.append((arg, base or default))
            for kw in call.keywords:
                default = _builder_default(kw.value)
                if default is not None:
                    hoists.append((kw.value, kw.arg or default))
        named = []
        for call, base in hoists:
            name, k = base, 1
            while name in taken:
                k += 1
                name = f"{base}{k}"
            taken.add(name)
            named.append((call, name))
        unprinted = []
        if (
            isinstance(stmt, ast.Assign)
            and _is_builder_call(stmt.value)
            and len(stmt.targets) == 1
            and isinstance(stmt.targets[0], ast.Name)
            and stmt.targets[0].id not in printed
        ):
            unprinted.append(stmt.targets[0].id)
        if named or unprinted:
            edits.append((stmt, named, unprinted))
    if not edits:
        return code
    for stmt, named, unprinted in reversed(edits):
        hoisted: list[str] = []
        for call, name in sorted(
            named, key=lambda cn: (cn[0].lineno, cn[0].col_offset), reverse=True
        ):
            hoisted.insert(0, f"{name} = {ast.get_source_segment(code, call)}")
            hoisted.insert(1, f"print({name})")
            _splice(lines, call, name)
        after = [f"print({name})" for name in unprinted]
        lines[_end(stmt) : _end(stmt)] = after
        lines[stmt.lineno - 1 : stmt.lineno - 1] = hoisted + ([""] if hoisted else [])
    return "\n".join(lines).rstrip() + "\n"


def structure_problems(code):
    """Return a list of house-format violations in a finished solution file."""
    problems = []
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return [f"syntax error: {e}"]
    if not (
        tree.body
        and isinstance(tree.body[0], ast.Expr)
        and isinstance(tree.body[0].value, ast.Constant)
        and isinstance(tree.body[0].value.value, str)
    ):
        problems.append("file must start with the description docstring")
    if "URL: https://leetcode.com" not in code:
        problems.append("docstring must contain the URL line")
    # house rule: zero imports unless genuinely needed. Imports of injected
    # modules are never needed (sanitize removes them); anything else (re,
    # random, ...) is allowed.
    for n in tree.body:
        redundant = (
            isinstance(n, ast.ImportFrom) and n.module in INJECTED_MODULES
        ) or (
            isinstance(n, ast.Import)
            and any(a.name in INJECTED_MODULES for a in n.names)
        )
        if redundant:
            problems.append("file imports from an injected module")
            break
    # ordinary problems define class Solution; design problems keep
    # leetcode's natural class name (Trie, NumArray, ...) per the house
    # convention, so any non-helper class satisfies this.
    if not any(
        isinstance(n, ast.ClassDef) and n.name not in HELPER_CLASSES for n in tree.body
    ):
        problems.append("file must define the problem's class")
    if "assert" not in code:
        problems.append("file must end with assert statements")
    return problems


def strip_solution(code):
    """Return `code` with class method bodies replaced by `pass` and every
    assert commented out. Prints stay live so the file still runs."""
    tree = ast.parse(code)
    src = code.splitlines()

    # start line -> (last line consumed, replacement lines)
    replace: dict[int, tuple[int, list[str]]] = {}
    commented: set[int] = set()

    # everything after the first-example demo call is the test block: it gets
    # commented wholesale (asserts AND any setup they need), so the whole
    # tail toggles back on with one cmd+/ in an editor.
    demo = next((s for s in tree.body if is_demo(s)), None)
    if demo is not None:
        live_defs: set[int] = set()
        for stmt in tree.body:
            # defs/classes stay live even after the demo (their bodies are
            # stripped separately); only plain statements join the block.
            if stmt.lineno <= _end(demo):
                continue
            if isinstance(stmt, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                live_defs.update(range(stmt.lineno, _end(stmt) + 1))
            else:
                commented.update(range(stmt.lineno, _end(stmt) + 1))
        # prose comments between block statements join the block too
        for i, line in enumerate(code.splitlines(), start=1):
            if i > _end(demo) and i not in live_defs and line.lstrip().startswith("#"):
                commented.add(i)

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name not in HELPER_CLASSES:
            for member in node.body:
                if not isinstance(member, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    continue
                body = member.body
                # leetcode ships some signatures with a docstring
                # ("modify nums in-place instead"); that is part of the
                # problem, so keep it and strip only what follows.
                if (
                    len(body) > 1
                    and isinstance(body[0], ast.Expr)
                    and isinstance(body[0].value, ast.Constant)
                    and isinstance(body[0].value.value, str)
                ):
                    body = body[1:]
                first, last = body[0], body[-1]
                if first.lineno == member.lineno:
                    # `def f(self): return 1` - keep the signature, drop the body
                    head = src[first.lineno - 1][: first.col_offset].rstrip()
                    body_indent = _indent_of(head) + "    "
                    replace[first.lineno] = (
                        _end(last),
                        [head, body_indent + "pass"],
                    )
                else:
                    body_indent = _indent_of(src[first.lineno - 1])
                    replace[first.lineno] = (_end(last), [body_indent + "pass"])
        elif isinstance(node, ast.Assert):
            commented.update(range(node.lineno, _end(node) + 1))

    out = []
    line_no = 1
    while line_no <= len(src):
        if line_no in replace:
            # `last` held an ast node above; here it is a line number
            last, replacement = replace[line_no]  # type: ignore[assignment]
            out.extend(replacement)
            line_no = last + 1  # type: ignore[operator]
            continue
        line = src[line_no - 1]
        if line_no in commented and line.strip():
            # existing comments get a second layer, so an editor's
            # uncomment-block action returns them to comments, not to code
            line = "# " + line
        out.append(line)
        line_no += 1

    return "\n".join(out).rstrip() + "\n"
