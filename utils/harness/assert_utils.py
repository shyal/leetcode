# assert_utils.py
#
# Comparisons for asserts in drills and solves, where the answer is
# right up to some order the problem does not fix.

import ast
import inspect
import os
import re
from typing import Any, Callable, Iterable, Sequence


def same_rows(a: Sequence[Iterable[Any]], b: Sequence[Iterable[Any]]) -> bool:
    """Row i of a and row i of b hold the same elements, in any order.

    The rows themselves stay in order: an adjacency list keyed by index.
    """
    return len(a) == len(b) and all(set(x) == set(y) for x, y in zip(a, b))


def same_seq(a: Iterable[Any], b: Iterable[Any]) -> bool:
    """The same elements in the same order, whatever the container.

    A tuple from divmod against a list in the assert: (1, 2) matches [1, 2].
    """
    return list(a) == list(b)


def uses(cls: type, *helpers: Callable[..., Any]) -> bool:
    """Every helper is called somewhere in the source of cls.

    Raises AssertionError naming the first helper cls never calls. The
    check reads the class as written, so it lives in the test block of a
    solve and goes with the asserts, never to leetcode.
    """
    called = _calls(cls)
    for h in helpers:
        if h.__name__ not in called:
            raise AssertionError(f"{cls.__name__} never calls {h.__name__}")
    return True


def avoids(cls: type, *helpers: Callable[..., Any]) -> bool:
    """No helper is called anywhere in the source of cls.

    The mirror of uses: for a drill whose rep is writing the helper by
    hand, so a call to the library version is a fail. Raises
    AssertionError naming the first helper cls calls.
    """
    called = _calls(cls)
    for h in helpers:
        if h.__name__ in called:
            raise AssertionError(f"{cls.__name__} calls {h.__name__}")
    return True


def folds(
    cls: type,
    op: str,
    start: bool = False,
    where: bool = False,
    block: bool = False,
) -> bool:
    """The mu source of cls has a fold of op (sum, max, min, count) with
    each form asked for: start is `from e`, where is `if cond`, block is
    a block in place of `: value`.

    The mu source is the `# mu <version>` block quoted above the class in
    its file. A Python solve has no such block and no fold to check, so
    it passes. Raises AssertionError naming the fold it did not find.
    """
    src = _mu_source(cls)
    if src is None:
        return True
    p = _mu_parser()(src)
    p.program()
    want = (start, where, block)
    for f_op, *have in p.folds:
        if f_op == op and all(h or not w for h, w in zip(have, want)):
            return True
    form = " ".join(
        [op]
        + ["from e"] * start
        + ["for x in xs"]
        + ["if cond"] * where
        + ["with a block" if block else ": value"]
    ).replace(" :", ":")
    raise AssertionError(f"{cls.__name__} has no fold `{form}`")


def _mu_source(cls: type) -> str | None:
    """The mu solution of cls. A class run from a mu file (`make` on
    current.mu) is that file's defs, above its script; one from a Python
    file is the solution quoted there under `# mu <version>`."""
    file = inspect.getsourcefile(cls) or ""
    src = open(file).read()
    if file.endswith(".mu"):
        p = _mu_parser()(src)
        p.program()
        end = (p.script_line or src.count("\n") + 2) - 1
        return "\n".join(src.split("\n")[:end])
    lines = src.split("\n")
    for k, line in enumerate(lines):
        if re.match(r"# mu \d", line):
            out = []
            for ln in lines[k + 1 :]:
                if not ln.startswith("#"):
                    break
                out.append(ln[2:] if ln.startswith("# ") else ln[1:])
            return "\n".join(out)
    return None


def _mu() -> Any:
    """mulang, with the leet profile loaded: mu/leetmu.py registers the
    pydsa helpers, so the transpiled class names the calls it makes."""
    import mulang

    mulang.profile(os.path.join(os.path.dirname(__file__), "..", ".."))
    return mulang


def _mu_parser() -> Any:
    """mu's Parser."""
    return _mu().Parser


def _class_source(cls: type) -> ast.AST:
    """The Python of cls as written: its source parsed, or, for a class run
    from a mu file, that file transpiled and the class picked out."""
    file = inspect.getsourcefile(cls) or ""
    if not file.endswith(".mu"):
        return ast.parse(inspect.getsource(cls))
    tree = ast.parse(_mu().transpile(open(file).read()))
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == cls.__name__:
            return node
    raise OSError(f"could not find class {cls.__name__} in {file}")


def _calls(cls: type) -> set[str]:
    """The names called in the source of cls: f(...) and m.f(...) both as f."""
    called = set()
    for node in ast.walk(_class_source(cls)):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Name):
            called.add(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            called.add(node.func.attr)
    return called
