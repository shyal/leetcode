"""mu on this repo: every example transpiles and passes the problem's cached
asserts, the grammar highlights every name the profile preloads, and
HARNESS.md links every spec.

The Python runs with `-S`, so no harness builtin leaks in: what passes
here is what LeetCode receives.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import leetmu  # noqa: E402, F401
import mulang  # noqa: E402
from mulang import VERSION, fmt, ide, transpile  # noqa: E402

MU_REPO = Path(mulang.__file__).parent.parent  # the mu repo, installed editable
CACHE = HERE.parent / ".prepare_cache"
EXAMPLES = sorted((HERE / "examples").glob("*.mu"))

# cached asserts whose input breaks the problem's stated constraints
OUTSIDE_CONSTRAINTS = {
    "0300": ["lengthOfLIS([])"],  # 1 <= nums.length
    "0743": ["], 10, 11, )"],  # 1 <= k <= n
    "0875": ["10**4, 1)", "[5, 5, 5, 5, 5], 3)", "[2, 2, 2, 2, 2], 2)"],  # n <= h
}


def asserts(stem):
    sol = json.loads((CACHE / f"{int(stem)}.json").read_text())["solution"]
    tail = sol[sol.index("\nsol = ") :]
    head, *rest = tail.split("\nassert")
    bad = OUTSIDE_CONSTRAINTS.get(stem, [])
    kept = [a for a in rest if not any(b in " ".join(a.split()) for b in bad)]
    assert len(rest) - len(kept) == len(bad), "an OUTSIDE_CONSTRAINTS entry went stale"
    return "\nassert".join([head] + kept)


@pytest.mark.parametrize("path", EXAMPLES, ids=lambda p: p.stem)
def test_example(path):
    code = transpile(path.read_text()) + asserts(path.stem)
    run = subprocess.run(
        [sys.executable, "-S", "-c", code], capture_output=True, text=True, timeout=60
    )
    assert run.returncode == 0, run.stderr[-2000:]


@pytest.mark.parametrize("path", EXAMPLES, ids=lambda p: p.stem)
def test_examples_are_formatted(path):
    assert fmt(path.read_text()) == path.read_text()


def test_vscode_grammar_highlights_every_helper():
    """The VS Code grammar's builtin rule names every mu helper and every
    harness helper sitecustomize preloads, so a new helper cannot ship
    without highlighting."""
    grammar_path = MU_REPO / "vscode" / "syntaxes" / "mu.tmLanguage.json"
    if not grammar_path.exists():
        pytest.skip("mu is not installed from its repo")
    grammar = json.loads(grammar_path.read_text())
    rule = grammar["repository"]["builtin"]["match"]
    listed = set(re.search(r"\\b\((.*?)\)\\b", rule).group(1).split("|"))
    # Grid and deep are pasted in by the transpiler, never written in mu
    helpers = set(ide.preloaded())
    assert helpers <= listed, sorted(helpers - listed)


def test_every_spec_version_is_linked_from_the_readme():
    """The current version has a spec, and HARNESS.md links every spec."""
    specs = sorted(p.name for p in (MU_REPO / "spec").glob("v*.md"))
    assert f"v{VERSION}.md" in specs
    harness = (HERE.parent / "HARNESS.md").read_text()
    linked = re.findall(r"\(\.\./mu/spec/(v[\d.]+\.md)\)", harness)
    assert sorted(linked) == specs


def test_run_file_asserts_report_the_values_they_saw(tmp_path):
    """`make` compiles the solve's bare `assert L == R` so a fail names both
    sides as the assert saw them: a side with side effects runs once, the
    line number is the assert's own, and the traceback starts at the file."""
    import io
    from contextlib import redirect_stderr

    sys.path.insert(0, str(Path(__file__).parent))
    import session

    f = tmp_path / "current.py"
    f.write_text(
        "from collections import deque\n"
        "d = deque([[1], [2]])\n"
        "assert d.popleft() == [2]\n"
    )
    err = io.StringIO()
    with redirect_stderr(err):
        status = session.run_file(f)
    assert status == 1
    lines = err.getvalue().splitlines()
    assert lines[0] == "Traceback (most recent call last):"
    assert lines[1] == f'  File "{f}", line 3, in <module>'
    assert lines[-2:] == ["AssertionError: left : [1]", "right: [2]"]

    # other operators are named; a chain or a message is left as written
    def fails(src):
        try:
            exec(session.compiled(src, "x"), {})
        except AssertionError as e:
            return str(e)

    assert fails("assert 1 is 2\n") == "left : 1\nright: 2\nop   : is"
    assert fails("assert 1 < 2 < 2\n") == ""
    assert fails("assert 1 == 2, 'm'\n") == "m"
