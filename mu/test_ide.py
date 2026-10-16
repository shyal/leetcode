"""mulang.ide on this repo: the leet profile's names complete and resolve,
a drill's import from dsa/ resolves, the hover types are mu types."""

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import leetmu  # noqa: E402, F401
from mulang import ide  # noqa: E402

# line 12 is half typed, line 13 never closes its bracket
TEXT = """# DRILL: Largest Of The Last K
# Example
from dsa.monotonic_queue import MonotonicQueue, Type

def largestOfLastK(nums: [int], k: int) -> [int]
  q = MonotonicQueue()
  res = []
  memo f(i, j) =
    | i == 0 -> 0
    | else -> f(i - 1, j)
  for >i, n in nums
    q.pu
    if x ==
    d = nbrs(grid, i,
    res <- f(i, 0)
  res

res = largestOfLastK([1], 1)
"""


def req(cmd, line, col, text=TEXT):
    return {"id": 1, "cmd": cmd, "root": ROOT, "text": text, "line": line, "col": col}


def test_an_unclosed_bracket_blanks_its_logical_line():
    assert ide.unclosed(TEXT.split("\n"))[1] == {13}
    assert ide.unclosed("x = f(a,\n      b)\ny = 1".split("\n"))[1] == set()
    assert ide.unclosed("x = f(a,\n b))\ny = 1".split("\n"))[1] == {0, 1}


def test_repair_blanks_only_the_broken_lines():
    code, origin, blanked = ide.repaired(TEXT.split("\n"))
    assert blanked == {12, 13}
    assert "res.append(f(i, 0))" in code
    assert origin[-1] == 18  # `res = largestOfLastK([1], 1)` is mu line 18, 1-based


def test_hover_gives_mu_types():
    assert ide.hover(req("hover", 4, 20))["contents"] == "```mu\nnums: [int]\n```"
    assert ide.hover(req("hover", 4, 32))["contents"] == "```mu\nk: int\n```"
    assert ide.hover(req("hover", 5, 2))["contents"] == "```mu\nq: MonotonicQueue\n```"
    assert ide.hover(req("hover", 6, 3))["contents"] == "```mu\nres: [int]\n```"
    assert ide.hover(req("hover", 10, 10))["contents"] == "```mu\nn: int\n```"


def test_hover_on_a_def_of_the_file_shows_its_line():
    assert ide.hover(req("hover", 14, 12))["contents"] == "```mu\nmemo f(i, j) =\n```"


def test_hover_on_a_helper_quotes_helpers_md():
    got = ide.hover(req("hover", 13, 10))["contents"]
    assert got.startswith("```mu\nnbrs(grid, i, j)")
    assert "nbrs(grid, p, eq=inf)" in got


def test_hover_on_nothing():
    assert ide.hover(req("hover", 1, 0)) is None  # a comment
    assert ide.hover(req("hover", 12, 4)) is None  # the half-typed `if`


def test_definition_of_a_name_is_its_mu_line():
    assert ide.definition(req("definition", 11, 4)) == [
        {"path": None, "line": 5, "col": 2}
    ]
    assert ide.definition(req("definition", 14, 12)) == [
        {"path": None, "line": 7, "col": 7}
    ]
    assert ide.definition(req("definition", 10, 15)) == [
        {"path": None, "line": 4, "col": 19}
    ]


def test_definition_of_an_import_is_its_class():
    [d] = ide.definition(req("definition", 5, 10))
    assert d["path"] == os.path.join(ROOT, "dsa", "monotonic_queue.py")
    assert d["line"] == 8


def test_definition_of_a_helper_is_its_pydsa_source():
    import pydsa.grid

    [d] = ide.definition(req("definition", 13, 10))
    assert d["path"] == pydsa.grid.__file__
    assert "def nbrs(" in open(d["path"]).read().split("\n")[d["line"]]


def test_completion_after_a_dot_lists_attributes():
    assert ide.complete(req("complete", 11, 8)) == [
        {"label": "push", "kind": "function"}
    ]


def test_completion_lists_scope_keywords_and_helpers():
    labels = {c["label"] for c in ide.complete(req("complete", 12, 4))}
    assert {
        "nums",
        "k",
        "q",
        "res",
        "f",
        "n",
        "while",
        "memo",
        "nbrs",
        "table",
    } <= labels
    assert "self" not in labels


def test_preloaded_names_are_the_harness_helpers():
    """A preloaded name is one sitecustomize injects that pydsa or utils/harness
    defines; the stdlib names it also injects are not."""
    names = ide.preloaded()
    assert {"nbrs", "linked_list_reverse_k", "draw_linked_list", "ListNode"} <= set(
        names
    )
    assert not {"deque", "Counter", "cache", "inf"} & set(names)


def test_completion_lists_every_harness_helper():
    """Every preloaded helper completes, not only the ones HELPERS.md lists."""
    labels = {c["label"] for c in ide.complete(req("complete", 12, 4))}
    missing = set(ide.preloaded()) - labels
    assert not missing, sorted(missing)


def test_completion_of_a_harness_helper_shows_its_def():
    text = TEXT.replace("    if x ==\n", "    linked_list\n")
    got = ide.complete(req("complete", 12, 15, text))
    assert [c["label"] for c in got] == ["linked_list_reverse_k"]
    assert got[0]["detail"].startswith("linked_list_reverse_k(h, k=inf)  # Reverse")


def test_hover_and_definition_of_a_harness_helper():
    text = TEXT.replace("    if x ==\n", "    linked_list_reverse_k(nums, 2)\n")
    hover = ide.hover(req("hover", 12, 8, text))["contents"]
    assert hover.startswith("```mu\nlinked_list_reverse_k(h, k=inf)")
    [d] = ide.definition(req("definition", 12, 8, text))
    import pydsa.linked

    assert d["path"] == pydsa.linked.__file__
    assert "def linked_list_reverse_k(" in open(d["path"]).read().split("\n")[d["line"]]


def test_signature_of_a_harness_helper():
    text = TEXT.replace("    if x ==\n", "    linked_list_reverse_k(nums, \n")
    got = ide.signature(req("signature", 12, 32, text))
    assert got["label"] == "linked_list_reverse_k(h, k=inf)"
    assert got["active"] == 1


def test_completion_filters_by_the_prefix():
    text = TEXT.replace("    if x ==\n", "    nb\n")
    got = ide.complete(req("complete", 12, 6, text))
    assert [c["label"] for c in got] == ["nbrs"]
    assert got[0]["detail"].startswith("nbrs(grid, i, j)")


def test_completion_in_a_loop_header():
    labels = [c["label"] for c in ide.complete(req("complete", 10, 17))]
    assert labels == ["nums", "num_digits"]


def test_signature_inside_a_call():
    got = ide.signature(req("signature", 13, 18))
    assert got["label"].startswith("nbrs(grid, r, c=None")
    assert got["active"] == 1
    assert got["doc"].startswith("nbrs(grid, i, j)")
    text = TEXT.replace("MonotonicQueue()", "MonotonicQueue(")
    got = ide.signature(req("signature", 5, 21, text))
    assert got["label"] == "MonotonicQueue(type: Type=Type.increasing)"
    assert ide.signature(req("signature", 6, 3)) is None


def test_a_bad_request_is_an_error_reply_not_a_crash():
    assert ide.answer({"id": 3, "cmd": "hover", "text": "", "line": 5, "col": 0}) == {
        "id": 3,
        "result": None,
    }
    assert "error" in ide.answer({"id": 4, "cmd": "nope", "text": ""})


def test_serve_round_trip():
    run = subprocess.run(
        [sys.executable, "-m", "mulang.ide"],
        input=json.dumps(req("hover", 5, 2)) + "\n",
        capture_output=True,
        text=True,
        cwd=ROOT,
        timeout=60,
    )
    assert run.returncode == 0, run.stderr
    assert json.loads(run.stdout) == {
        "id": 1,
        "result": {"contents": "```mu\nq: MonotonicQueue\n```"},
    }
