"""The judge queue (settled 2026-09-06). `make solved` used to wait for the
judge - a median 38s, up to 3 minutes, per drill - before it committed.
Now the file phase writes a placeholder entry (the rep, on the drill's
TRAINS, pending) and commits at once; the judge runs detached and lands its
verdict in its own commit, on whatever is checked out when it finishes.
These pin the placeholder's shape, the concurrent write, and the commit
rule (amend the solve's own unpushed commit, otherwise a judge: commit that
never sweeps current.py)."""

import json
import os
import subprocess
from datetime import datetime, timezone
from importlib.machinery import SourceFileLoader

import pytest

from kg import kg_lib

KG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "kg")
kg_extract = SourceFileLoader("kg_extract_q", os.path.join(KG, "kg_extract")).load_module()

NODES = {"sliding-window": {}, "prefix-sum": {}, "two-pointers": {}}
PROBLEMS = {"1539": {"moves": ["two-pointers", "prefix-sum"]}}

DRILL = '''"""
DRILL: Slide, Never Shrink
TRAINS: sliding-window, prefix-sum
Grow the window.

---
asked for a walkthrough on the shrink step
"""
class Solution:
    pass
'''


@pytest.fixture
def graph(tmp_path, monkeypatch):
    g = tmp_path / "graph"
    g.mkdir()
    (g / "evidence.json").write_text(json.dumps({"evidence": {}}))
    monkeypatch.setattr(kg_lib, "GRAPH_DIR", str(g))
    (tmp_path / "solved").mkdir()
    monkeypatch.chdir(tmp_path)
    return tmp_path


def write(root, name, text):
    p = root / "solved" / name
    p.write_text(text)
    return os.path.join("solved", name)


# --- the placeholder ------------------------------------------------------------

def test_placeholder_is_the_rep_on_the_trains_nodes(graph):
    path = write(graph, "d_Slide_Never_Shrink_2026_09_06T04_31_57_473199_00_00Z.py", DRILL)
    e = kg_extract.stub_entry(path, NODES, PROBLEMS, now=datetime(2026, 9, 6, 4, 32, tzinfo=timezone.utc))
    assert e["problem"] == "drill"
    assert e["date"] == "2026-09-06"
    assert e["moves"] == {"sliding-window": "clean", "prefix-sum": "clean"}
    assert e[kg_lib.PENDING] == "2026-09-06T04:32:00+00:00"


def test_placeholder_reads_the_assist_word_from_the_notes(graph):
    """The level word in the notes is the mark; the judge's floor reads it
    and so must the placeholder, or a walked-through drill counts as an
    unaided rep for the minute the judge takes."""
    path = write(graph, "d_Slide_Never_Shrink_2026_09_06T04_31_57_473199_00_00Z.py", DRILL)
    e = kg_extract.stub_entry(path, NODES, PROBLEMS)
    assert e["assist"] == {"sliding-window": "walkthrough", "prefix-sum": "walkthrough"}


def test_placeholder_of_a_problem_is_its_canonical_walk(graph):
    path = write(graph, "p1539_Kth_Missing_2026_09_05T21_08_16_000000_00_00Z.py",
                 '"""\n1539. Kth Missing\n"""\nclass Solution:\n    pass\n')
    e = kg_extract.stub_entry(path, NODES, PROBLEMS)
    assert e["problem"] == "1539"
    assert e["moves"] == {"two-pointers": "clean", "prefix-sum": "clean"}
    assert "assist" not in e


def test_placeholder_of_a_failed_file_marks_no_move(graph):
    """A failed solve records the rep with no verdicts: the stub cannot see
    which move the defect is in, so it condemns none of them."""
    path = write(graph, "d_Slide_Never_Shrink_FAILED_2026_09_06T04_31_57_473199_00_00Z.py", DRILL)
    e = kg_extract.stub_entry(path, NODES, PROBLEMS)
    assert e["moves"] == {} and e[kg_lib.PENDING] and e["problem"] == "drill"


def test_unknown_trains_are_dropped_and_the_rep_still_exists(graph):
    path = write(graph, "d_X_2026_09_06T04_31_57_473199_00_00Z.py",
                 '"""\nDRILL: X\nTRAINS: no-such-node\n"""\n')
    e = kg_extract.stub_entry(path, NODES, PROBLEMS)
    assert e["moves"] == {} and e[kg_lib.PENDING]


# --- two writers, one file ------------------------------------------------------

def test_a_landing_judge_does_not_clobber_the_next_placeholder(graph):
    """The worker loaded evidence a minute ago; `make solved` wrote the next
    solve's placeholder since. The worker's write must keep it."""
    stale = kg_lib.load_evidence()  # what the worker holds
    kg_lib.store_evidence_entry("solved/next.py", {"date": "2026-09-06", "moves": {}, "pending": "x"})
    assert "solved/next.py" not in stale
    fresh = kg_lib.store_evidence_entry("solved/judged.py", {"date": "2026-09-06", "moves": {"prefix-sum": "clean"}})
    assert set(fresh) == {"solved/next.py", "solved/judged.py"}
    assert set(kg_lib.load_evidence()) == {"solved/next.py", "solved/judged.py"}


def test_pending_lists_placeholders_oldest_first(graph):
    old = datetime(2026, 9, 6, 4, 0, tzinfo=timezone.utc).isoformat()
    new = datetime.now(timezone.utc).isoformat()
    ev = {"a": {"pending": new}, "b": {"pending": old}, "c": {"moves": {}}}
    out = kg_lib.pending_judgements(ev)
    assert [p for p, _ in out] == ["b", "a"]
    assert out[0][1] > kg_lib.PENDING_STALE_SECONDS > out[1][1]


# --- the commit rule -------------------------------------------------------------

def git(root, *args):
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=True).stdout


@pytest.fixture
def repo(graph, monkeypatch):
    root = str(graph)
    git(root, "init", "-q", "-b", "master")
    git(root, "config", "user.email", "t@t")
    git(root, "config", "user.name", "t")
    monkeypatch.setattr(kg_extract, "REPO_ROOT", root)
    path = write(graph, "d_Slide_Never_Shrink_2026_09_06T04_31_57_473199_00_00Z.py", DRILL)
    (graph / "current.py").write_text("")
    git(root, "add", ".")
    git(root, "commit", "-qm", "drill: Slide, Never Shrink\n\nsolve time: 1m 2s")
    return root, path


def judged_entry():
    return {"date": "2026-09-06", "problem": "drill", "moves": {"sliding-window": "struggled"},
            "summary": "The loop grows r and never shrinks."}


def tracked_status(root):
    return [l for l in git(root, "status", "--porcelain").splitlines() if not l.startswith("??")]


def commits(root, ref="HEAD"):
    return git(root, "log", "--format=%s", ref).split("\n")[:-1]


def test_the_judge_folds_into_the_solves_commit_when_it_is_head(repo):
    root, path = repo
    kg_lib.store_evidence_entry(path, judged_entry())
    open(os.path.join(root, "current.py"), "w").write("# half typed next solve")
    out = kg_extract.commit_judgement([(path, judged_entry())], refit=False)
    assert out == "judge: folded into drill: Slide, Never Shrink"
    assert commits(root) == ["drill: Slide, Never Shrink"]
    assert tracked_status(root) == [" M current.py"]  # never swept in
    shown = git(root, "show", "--name-only", "--format=", "HEAD").split()
    assert "graph/evidence.json" in shown and "current.py" in shown
    assert "never shrinks" in git(root, "show", "HEAD:graph/evidence.json")


def test_the_judge_folds_from_the_next_branch_and_rebases_it(repo):
    """The next drill is already prepared (its branch's first commit is
    HEAD) and half typed. The verdict goes into the solve's commit on
    master, the branch is replayed onto it, and the working tree does not
    move: same tree, current.py still dirty."""
    root, path = repo
    git(root, "checkout", "-qb", "2")
    open(os.path.join(root, "current.py"), "w").write("# statement of the next one")
    git(root, "commit", "-qam", "Next")
    open(os.path.join(root, "current.py"), "w").write("# statement of the next one\n# and my half solve")
    kg_lib.store_evidence_entry(path, judged_entry())
    out = kg_extract.commit_judgement([(path, judged_entry())], refit=False)
    assert out.startswith("judge: folded into")
    assert git(root, "rev-parse", "--abbrev-ref", "HEAD").strip() == "2"
    assert commits(root, "master") == ["drill: Slide, Never Shrink"]
    assert commits(root, "2") == ["Next", "drill: Slide, Never Shrink"]
    assert git(root, "merge-base", "master", "2").strip() == git(root, "rev-parse", "master").strip()
    assert "never shrinks" in git(root, "show", "master:graph/evidence.json")
    assert tracked_status(root) == [" M current.py"]
    assert open(os.path.join(root, "current.py")).read().endswith("my half solve")
    # nothing left for the squash-merge to conflict on
    git(root, "stash", "-q")
    git(root, "checkout", "-q", "master")
    git(root, "merge", "-q", "--squash", "2")


def test_the_judge_rebases_a_parked_branch_too(repo):
    """make sleep parked the next solve's branch and returned to master
    while the judge was out: that branch was cut from the solve's commit and
    is rebased onto the rewritten one, dates kept."""
    root, path = repo
    git(root, "checkout", "-qb", "parked")
    open(os.path.join(root, "current.py"), "w").write("# parked statement")
    git(root, "commit", "-qam", "Parked")
    git(root, "commit", "-q", "--allow-empty", "-m", "sleeping: 2. Parked")
    stamp = git(root, "show", "-s", "--format=%at %ct", "parked").strip()
    git(root, "checkout", "-q", "master")
    kg_lib.store_evidence_entry(path, judged_entry())
    out = kg_extract.commit_judgement([(path, judged_entry())], refit=False)
    assert out.startswith("judge: folded into")
    assert commits(root, "parked") == ["sleeping: 2. Parked", "Parked", "drill: Slide, Never Shrink"]
    assert git(root, "merge-base", "master", "parked").strip() == git(root, "rev-parse", "master").strip()
    assert git(root, "show", "-s", "--format=%at %ct", "parked").strip() == stamp


def test_the_judge_never_rewrites_a_pushed_solve(repo):
    root, path = repo
    git(root, "update-ref", "refs/remotes/origin/master", "HEAD")
    kg_lib.store_evidence_entry(path, judged_entry())
    out = kg_extract.commit_judgement([(path, judged_entry())], refit=False)
    assert out.startswith("judge: committed judge: Slide Never Shrink (solve already pushed")
    assert commits(root) == ["judge: Slide Never Shrink", "drill: Slide, Never Shrink"]
    body = git(root, "log", "-1", "--format=%b")
    assert "sliding-window=struggled" in body and "never shrinks" in body


def test_a_branch_that_does_not_replay_keeps_the_judges_commit_on_top(repo):
    """A branch that edited the same evidence lines (a hand edit) cannot be
    rebased silently: nothing is rewritten, the judge: commit stands."""
    root, path = repo
    git(root, "checkout", "-qb", "2")
    ev = os.path.join(root, "graph", "evidence.json")
    open(ev, "w").write(json.dumps({"evidence": {path: {"date": "2026-09-06", "moves": {"prefix-sum": "clean"}}}}))
    git(root, "commit", "-qam", "hand edit")
    git(root, "checkout", "-q", "master")
    before = git(root, "rev-parse", "master", "2")
    kg_lib.store_evidence_entry(path, judged_entry())
    out = kg_extract.commit_judgement([(path, judged_entry())], refit=False)
    assert "(not folded:" in out and "does not replay cleanly on 2" in out
    assert git(root, "rev-parse", "master", "2") != before  # master carries the judge: commit
    assert commits(root, "master") == ["judge: Slide Never Shrink", "drill: Slide, Never Shrink"]
    assert commits(root, "2") == ["hand edit", "drill: Slide, Never Shrink"]
    assert not os.path.exists(os.path.join(root, ".git", "worktrees")) or \
        git(root, "worktree", "list").count("\n") == 1


def test_judge_titles():
    assert kg_extract.judge_title("solved/d_Slide_Never_Shrink_2026_09_06T04_31_57_473199_00_00Z.py") == "Slide Never Shrink"
    assert kg_extract.judge_title("solved/p542_01_Matrix_FAILED_2026_09_03T03_48_58_768516_00_00Z.py") == "542. 01 Matrix"
