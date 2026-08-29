"""Derive a candidate stub from a validated solution.

The prepare cache stores the full solution that passed its own asserts; the
stub written to `current.py` is derived from it here. The transform is
line-based and driven by `ast`, so the docstring, spacing and comments of the
original survive byte-for-byte - only method bodies and asserts are touched.
"""

import ast

# injected by sitecustomize; if a generator redefines one anyway, leave it
# working rather than gutting it and breaking the file.
HELPER_CLASSES = {"TreeNode", "ListNode", "GraphNode", "Node"}


# modules whose contents sitecustomize already injects; importing from them
# is always redundant in a solve file.
INJECTED_MODULES = {
    "typing", "collections", "functools", "itertools", "math",
    "heapq", "bisect", "string",
}


def _indent_of(line):
    return line[: len(line) - len(line.lstrip())]


def sanitize(code):
    """Remove top-level statements a generator emits out of habit that the
    sitecustomize environment makes redundant: imports from injected modules
    and redefinitions of the helper classes. Returns the cleaned source."""
    tree = ast.parse(code)
    drop = set()
    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and node.module in INJECTED_MODULES:
            drop.update(range(node.lineno, node.end_lineno + 1))
        elif isinstance(node, ast.Import) and all(
            a.name in INJECTED_MODULES for a in node.names
        ):
            drop.update(range(node.lineno, node.end_lineno + 1))
        elif isinstance(node, ast.ClassDef) and node.name in HELPER_CLASSES:
            drop.update(range(node.lineno, node.end_lineno + 1))
    if not drop:
        return code
    src = code.splitlines()
    out = [l for i, l in enumerate(src, start=1) if i not in drop]
    # collapse the blank run left where a block was removed
    text = "\n".join(out)
    while "\n\n\n\n" in text:
        text = text.replace("\n\n\n\n", "\n\n\n")
    return text.lstrip("\n").rstrip() + "\n"


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
        isinstance(n, ast.ClassDef) and n.name not in HELPER_CLASSES
        for n in tree.body
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
    replace = {}
    commented = set()

    # everything after the first-example demo call is the test block: it gets
    # commented wholesale (asserts AND any setup they need), so the whole
    # tail toggles back on with one cmd+/ in an editor.
    def is_demo(stmt):
        if not (isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call)):
            return False
        fn = stmt.value.func
        name = fn.id if isinstance(fn, ast.Name) else getattr(fn, "attr", "")
        return name in {"print", "tabulate", "rich_print"} or name.startswith("draw_")

    demo = next((s for s in tree.body if is_demo(s)), None)
    if demo is not None:
        live_defs = set()
        for stmt in tree.body:
            # defs/classes stay live even after the demo (their bodies are
            # stripped separately); only plain statements join the block.
            if stmt.lineno <= demo.end_lineno:
                continue
            if isinstance(stmt, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                live_defs.update(range(stmt.lineno, stmt.end_lineno + 1))
            else:
                commented.update(range(stmt.lineno, stmt.end_lineno + 1))
        # prose comments between block statements join the block too
        for i, line in enumerate(code.splitlines(), start=1):
            if (
                i > demo.end_lineno
                and i not in live_defs
                and line.lstrip().startswith("#")
            ):
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
                    replace[first.lineno] = (last.end_lineno, [head, body_indent + "pass"])
                else:
                    body_indent = _indent_of(src[first.lineno - 1])
                    replace[first.lineno] = (last.end_lineno, [body_indent + "pass"])
        elif isinstance(node, ast.Assert):
            commented.update(range(node.lineno, node.end_lineno + 1))

    out = []
    line_no = 1
    while line_no <= len(src):
        if line_no in replace:
            last, replacement = replace[line_no]
            out.extend(replacement)
            line_no = last + 1
            continue
        line = src[line_no - 1]
        if line_no in commented and line.strip():
            # existing comments get a second layer, so an editor's
            # uncomment-block action returns them to comments, not to code
            line = "# " + line
        out.append(line)
        line_no += 1

    return "\n".join(out).rstrip() + "\n"
