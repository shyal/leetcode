"""The mu side of a solve: stub at serve, run while solving, fold at solved."""

import glob
import json
import os
import re
import shutil
import subprocess
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path[:0] = [HERE, os.path.join(ROOT, "utils", "tests")]
from mulang import VERSION, Parser, transpile  # noqa: E402
from session import highlighted  # noqa: E402
from session import SETUP, stub, title  # noqa: E402
from test_reference_solutions import PY, drill_for  # noqa: E402

REFERENCES = sorted(
    glob.glob(os.path.join(ROOT, "graph", "node_notes", "*", "d[0-9]*.mu"))
)
SESSION = os.path.join(HERE, "session.py")
ENV = dict(
    os.environ,
    PYTHONPATH=os.pathsep.join(
        [ROOT, os.path.join(ROOT, "utils"), os.path.join(ROOT, "utils", "harness")]
    ),
)


def reference(prefix):
    return next(r for r in REFERENCES if os.path.basename(r).startswith(prefix))


def signatures(src):
    """The (name, parameters) of every def, methods included, and the base
    class of the first class."""
    p = Parser(src)
    sigs, base = [], None
    for d in p.program():
        if d[0] == "class":
            base = d[2] if d[1] == "Solution" else base
            sigs += [(b[1], [n for n, _ in b[2]]) for b in d[3] if b[0] == "def"]
        elif d[0] == "def":
            sigs.append((d[1], [n for n, _ in d[2]]))
    return sigs, base


def solved(stub_text, reference_text, note=""):
    """current.mu as the operator leaves it: the stub's statement block,
    with a note under `# ---`, the reference solution in place of the empty
    defs, and every assert of the script turned on."""
    lines = stub_text.split("\n")
    first = next(
        i for i, ln in enumerate(lines) if ln.startswith(("class ", "def ", "@"))
    )
    head = lines[:first]
    if note:
        head.insert(head.index("# ---") + 1, f"# {note}")
    p = Parser(stub_text)
    p.program()
    script = lines[p.script_line - 1 :] if p.script_line else []
    script = [re.sub(rf"^# ({SETUP}.*)$", r"\1", ln) for ln in script]
    body = reference_text.split("\n")
    while body and body[0].startswith("#"):
        body.pop(0)  # the # REFERENCE line
    return "\n".join(head + body + [""] + script) + "\n"


def session(cwd, *args):
    return subprocess.run(
        [PY, SESSION, *args],
        cwd=cwd,
        env=ENV,
        capture_output=True,
        text=True,
        timeout=120,
    )


def python(cwd, name="current.py"):
    return subprocess.run(
        [PY, name], cwd=cwd, env=ENV, capture_output=True, text=True, timeout=120
    )


@pytest.mark.parametrize("ref", REFERENCES, ids=os.path.basename)
def test_every_drill_gets_a_stub_with_the_reference_signature(ref):
    s = stub(open(drill_for(ref)).read())
    transpile(s)
    assert signatures(s) == signatures(open(ref).read())
    assert s.startswith("# ") and "\n# ---\n" in s
    assert not re.search(r"^# (DRILL|TRAINS):", s, flags=re.M)


@pytest.mark.parametrize("ref", REFERENCES, ids=os.path.basename)
def test_every_drill_runs_green_from_current_mu(ref, tmp_path):
    drill = open(drill_for(ref)).read()
    (tmp_path / "current.py").write_text(drill)
    (tmp_path / "current.mu").write_text(solved(stub(drill), open(ref).read()))
    run = session(tmp_path, "run")
    assert run.returncode == 0, run.stdout[-1500:] + run.stderr[-1500:]
    assert "Running from current.mu." in run.stderr


def test_the_stub_translates_the_asserts():
    s = stub(
        open(
            os.path.join(ROOT, "drills/binary-search-on-answer/d115_first_true.py")
        ).read()
    )
    assert "# assert sol.firstTrue(1, 100, x -> x * x >= 50) == 8" in s
    s = stub(
        open(
            os.path.join(ROOT, "drills/fast-slow-pointers/d109_cut_at_the_middle.py")
        ).read()
    )
    assert "def cut(vals)\n  first, second = sol.cutAtTheMiddle(" in s
    assert (
        "print(get_list_values(first), get_list_values(second))  # [1, 2, 3] [4, 5]"
        in s
    )
    s = stub(
        open(
            os.path.join(ROOT, "drills/event-sweep/d119_turn_knobs_to_a_total.py")
        ).read()
    )
    assert "    def band(a, b)\n      (min(a, b) + 1, max(a, b) + limit)\n" in s


# one drill of each shape: a callable argument, a class built as `p =`,
# a base class, a helper in the stub, multi-line asserts, a tree
CASES = ["d115_", "d17_", "d71_", "d119_", "d2_", "d68_"]


@pytest.mark.parametrize("prefix", CASES)
def test_a_whole_session(prefix, tmp_path):
    ref = reference(prefix)
    (tmp_path / "current.py").write_text(open(drill_for(ref)).read())

    assert session(tmp_path, "stub").returncode == 0
    served = (tmp_path / "current.mu").read_text()
    assert served == (tmp_path / ".mu_stub").read_text()
    # the stub alone is not a solve: current.py runs as served
    assert "Running from current.mu." not in session(tmp_path, "run").stderr

    (tmp_path / "current.mu").write_text(
        solved(served, open(ref).read(), "peeked at the loop")
    )
    run = session(tmp_path, "run")
    assert run.returncode == 0, run.stdout[-1500:] + run.stderr[-1500:]

    # serving the same drill again never overwrites the work
    assert "left alone" in session(tmp_path, "stub").stdout

    assert session(tmp_path, "fold").returncode == 0
    folded = (tmp_path / "current.py").read_text()
    assert folded.startswith('"""')
    doc = folded.split('"""')[1]
    assert "\n---\npeeked at the loop\n" in doc  # the notes, where the judge reads them
    quoted = folded.split(f"# mu {VERSION}\n")[1].split("\n\n")[0]
    assert "# class Solution" in quoted
    assert "# DRILL" not in quoted and "# assert" not in quoted
    ran = python(tmp_path)
    assert ran.returncode == 0, ran.stdout[-1500:] + ran.stderr[-1500:]

    # file: current.mu is what solved/ keeps, and it runs alone with mu
    work = (tmp_path / "current.mu").read_text()
    assert session(tmp_path, "file").returncode == 0
    archived = (tmp_path / "current.mu").read_text()
    assert (tmp_path / "current.py").read_text() == ""
    assert not (tmp_path / ".mu_stub").exists()
    assert f"\n\n# mu {VERSION}\n" in archived
    assert archived.split("\n\n")[0] == work.split("\n\n")[0]  # the statement and notes
    ran = subprocess.run(
        [PY, "-m", "mulang", "current.mu"],
        cwd=tmp_path, env=ENV, capture_output=True, text=True, timeout=120,
    )
    assert ran.returncode == 0, ran.stdout[-1500:] + ran.stderr[-1500:]


def test_file_puts_the_leetcode_verdict_in_the_notes(tmp_path):
    """lc_submit writes the verdict into the folded current.py's docstring;
    file carries it into current.mu, last in the notes, where the judge
    reads it (kg::lang::notes_of)."""
    ref = reference("d115_")
    (tmp_path / "current.py").write_text(open(drill_for(ref)).read())
    session(tmp_path, "stub")
    served = (tmp_path / "current.mu").read_text()
    (tmp_path / "current.mu").write_text(solved(served, open(ref).read(), "no help"))
    session(tmp_path, "fold")
    py = (tmp_path / "current.py").read_text()
    (tmp_path / "current.py").write_text(py.replace("no help\n", "no help\nLEETCODE: Accepted\n", 1))
    session(tmp_path, "file")
    head = (tmp_path / "current.mu").read_text().split("\n\n")[0]
    assert head.endswith("# ---\n# no help\n# LEETCODE: Accepted")


def test_file_without_mu_work_empties_the_stub(tmp_path):
    """A drill solved in current.py: file leaves current.py to be archived
    and empties current.mu, which held only the stub."""
    shutil.copy(drill_for(reference("d115_")), tmp_path / "current.py")
    session(tmp_path, "stub")
    py = (tmp_path / "current.py").read_text()
    assert session(tmp_path, "file").returncode == 0
    assert (tmp_path / "current.py").read_text() == py
    assert (tmp_path / "current.mu").read_text() == ""
    assert not (tmp_path / ".mu_stub").exists()


def test_serving_another_drill_keeps_the_old_work(tmp_path):
    first, second = reference("d115_"), reference("d120_")
    (tmp_path / "current.py").write_text(open(drill_for(first)).read())
    session(tmp_path, "stub")
    work = solved((tmp_path / "current.mu").read_text(), open(first).read())
    (tmp_path / "current.mu").write_text(work)
    (tmp_path / "current.py").write_text(open(drill_for(second)).read())
    assert "moved to current.mu.prev" in session(tmp_path, "stub").stdout
    assert (tmp_path / "current.mu.prev").read_text() == work
    assert (tmp_path / "current.mu").read_text().startswith(
        f"# {title(open(drill_for(second)).read())}\n"
    )


def test_a_current_mu_for_another_drill_is_not_run(tmp_path):
    shutil.copy(drill_for(reference("d120_")), tmp_path / "current.py")
    (tmp_path / "current.mu").write_text(
        stub(open(drill_for(reference("d115_"))).read())
    )
    run = session(tmp_path, "run")
    assert "current.mu" not in run.stderr


def test_drill_fill_leaves_the_heaviest_lines_of_the_latest_solve(tmp_path):
    """DRILL_FILL: the drill server writes .mu_fill naming the drill by
    its id, the one .drill.json names; the statement says nothing. The stub gives the solved file's mu solve with
    its heaviest half put as `pass` (the prefix sums and the answer), setup
    and the count kept, and the filled stub still runs."""
    ref = reference("d11_")
    (tmp_path / "solved").mkdir()
    (tmp_path / "solved" / "d_x.py").write_text(
        f"# mu {VERSION}\n"
        + "".join(f"# {ln}\n" for ln in open(ref).read().split("\n")[1:])
    )
    drill = open(drill_for(ref)).read()
    (tmp_path / "current.py").write_text(drill)
    assert "DRILL_FILL" not in drill
    (tmp_path / ".drill.json").write_text(json.dumps({"drill": "d11"}))
    fill = {"drill": "d11", "source": "solved/d_x.py", "blank": [1, 2]}
    (tmp_path / ".mu_fill").write_text(json.dumps(fill))
    assert "DRILL_FILL gives" in session(tmp_path, "stub").stdout
    mu = (tmp_path / "current.mu").read_text()
    assert "    count = table(101" in mu and "      count[x] += 1\n" in mu
    assert "    pass\n    pass\n" in mu and "scan" not in mu
    transpile(mu)

    # a solve archived as .mu gives the same fill
    (tmp_path / "solved" / "d_y.mu").write_text(
        f"# {title(drill)}\n#\n# ---\n\n# mu {VERSION}\n\n" + open(ref).read().split("\n", 1)[1]
    )
    fill["source"] = "solved/d_y.mu"
    (tmp_path / ".mu_fill").write_text(json.dumps(fill))
    (tmp_path / "current.mu").write_text("")
    assert "DRILL_FILL gives" in session(tmp_path, "stub").stdout
    assert (tmp_path / "current.mu").read_text() == mu


def test_drill_fill_is_left_out_for_another_drill(tmp_path):
    (tmp_path / "current.py").write_text(open(drill_for(reference("d11_"))).read())
    (tmp_path / ".drill.json").write_text(json.dumps({"drill": "d11"}))
    fill = {"drill": "d12", "source": "solved/d_x.py", "blank": [1, 2]}
    (tmp_path / ".mu_fill").write_text(json.dumps(fill))
    assert "DRILL_FILL" not in session(tmp_path, "stub").stdout


def test_a_mu_syntax_error_names_the_line(tmp_path):
    drill = drill_for(reference("d115_"))
    shutil.copy(drill, tmp_path / "current.py")
    (tmp_path / "current.mu").write_text(
        f"# {title(open(drill).read())}\ndef firstTrue(lo: int) -> int\n  x = \n"
    )
    run = session(tmp_path, "run")
    assert run.returncode == 1
    assert run.stderr.startswith("current.mu: line 3:")


def test_a_failed_assert_names_the_mu_line(tmp_path):
    shutil.copy(drill_for(reference("d115_")), tmp_path / "current.py")
    session(tmp_path, "stub")
    served = (tmp_path / "current.mu").read_text()
    work = solved(served, reference_wrong("d115_"))
    (tmp_path / "current.mu").write_text(work)
    run = session(tmp_path, "run")
    assert run.returncode == 1
    lines = work.split("\n")
    first = next(k for k, ln in enumerate(lines, 1) if ln.startswith("assert "))
    assert f'current.mu", line {first}, in <module>\n    {lines[first - 1]}\n' in (
        run.stderr
    )
    assert "AssertionError: left : " in run.stderr
    # nothing is written: the mu runs in place
    assert not (tmp_path / ".mu_current.py").exists()
    assert ".mu_current.py" not in run.stderr


def reference_wrong(prefix):
    """A reference solution with its last line's value off by one."""
    text = open(reference(prefix)).read().rstrip("\n")
    return text + " + 1\n"


def test_an_exception_in_the_solution_names_the_mu_line(tmp_path):
    (tmp_path / "current.py").write_text(PROBLEM)
    session(tmp_path, "stub")
    work = (tmp_path / "current.mu").read_text()
    body = "  def twoSum(nums: [int], target: int) -> [int]\n    seen = {}\n    nums[len(nums)]\n"
    work = work.replace(
        "  def twoSum(nums: [int], target: int) -> [int]\n    pass\n", body
    )
    work = work.replace("# assert", "assert")
    (tmp_path / "current.mu").write_text(work)
    run = session(tmp_path, "run")
    assert run.returncode == 1
    at = work.split("\n").index("    nums[len(nums)]") + 1
    assert f'current.mu", line {at}, in twoSum\n    nums[len(nums)]\n' in run.stderr
    assert run.stderr.rstrip().endswith("IndexError: list index out of range")


def test_a_frame_in_a_pasted_helper_shows_its_own_source(tmp_path):
    (tmp_path / "current.py").write_text(PROBLEM)
    session(tmp_path, "stub")
    work = (tmp_path / "current.mu").read_text()
    body = (
        "  def twoSum(nums: [int], target: int) -> [int]\n"
        "    [first_true(0, 3, x -> nums[x + 10] > 0)]\n"
    )
    work = work.replace(
        "  def twoSum(nums: [int], target: int) -> [int]\n    pass\n", body
    )
    work = work.replace("# assert", "assert")
    (tmp_path / "current.mu").write_text(work)
    run = session(tmp_path, "run")
    assert run.returncode == 1
    helper = 'File "<mu helpers>", line '
    assert helper in run.stderr
    shown = run.stderr.split(helper)[1].split("\n")[1]
    assert shown.strip() == "return lo + bisect_left(range(lo, hi + 1), True, key=ok)"
    at = work.split("\n").index("    [first_true(0, 3, x -> nums[x + 10] > 0)]") + 1
    assert f'current.mu", line {at}, in <lambda>' in run.stderr


def test_the_avoids_gate_reads_the_class_through_the_transpiler(tmp_path):
    drill = open(drill_for(reference("d123_"))).read()
    (tmp_path / "current.py").write_text(drill)
    served = stub(drill)
    head = "  def byRatio(classes: [[int]]) -> [[int]]\n    pass\n"
    assert head in served
    work = served.replace(head, head.replace("pass", "classes.sort()\n    classes"))
    work = work.replace("# assert avoids", "assert avoids")
    (tmp_path / "current.mu").write_text(work)
    run = session(tmp_path, "run")
    assert run.returncode == 1
    assert run.stderr.rstrip().endswith("AssertionError: Solution calls sort")
    (tmp_path / "current.py").write_text(
        PROBLEM.replace("# assert", 'assert folds(Solution, "sum")\n# assert')
    )
    session(tmp_path, "stub")
    served = (tmp_path / "current.mu").read_text()
    served = served.replace("# assert folds", "assert folds")
    head = "  def twoSum(nums: [int], target: int) -> [int]\n    pass\n"
    assert head in served
    plain = served.replace(
        head, "  def twoSum(nums: [int], target: int) -> [int]\n    [sum(nums)]\n"
    )
    (tmp_path / "current.mu").write_text(plain)
    run = session(tmp_path, "run")
    assert run.returncode == 1
    assert "Solution has no fold `sum for x in xs: value`" in run.stderr
    folded = served.replace(
        head,
        "  def twoSum(nums: [int], target: int) -> [int]\n    [sum for x in nums: x]\n",
    )
    (tmp_path / "current.mu").write_text(folded)
    assert session(tmp_path, "run").returncode == 0
    # a fold in the script, under the asserts, does not count
    (tmp_path / "current.mu").write_text(plain + "\ntotal = sum for x in [1, 2]: x\n")
    assert session(tmp_path, "run").returncode == 1
    # filed into current.py, the gate reads the quoted mu block there
    session(tmp_path, "fold")
    assert "no fold" in python(tmp_path).stderr


def test_the_traceback_is_coloured_on_request(tmp_path):
    (tmp_path / "current.py").write_text(PROBLEM)
    session(tmp_path, "stub")
    work = (tmp_path / "current.mu").read_text().replace("# assert", "assert")
    (tmp_path / "current.mu").write_text(work)
    plain = session(tmp_path, "run").stderr  # a pipe: no colour
    assert "\033[" not in plain
    run = session(tmp_path, "run", "--color")
    assert run.returncode == 1
    at = work.split("\n").index("assert sol.twoSum([2, 7, 11, 15], 9) == [0, 1]") + 1
    assert f'File "\033[2mcurrent.mu\033[0m", line \033[33m{at}\033[0m' in run.stderr
    left = "\033[31m\033[1mAssertionError\033[0m: \033[31mleft :\033[0m"
    assert left + highlighted(" None") in run.stderr
    assert "\033[32mright:\033[0m" + highlighted(" [0, 1]") in run.stderr
    assert "\033[" not in session(tmp_path, "run", "--no-color").stderr


def test_any_mu_file_runs_on_its_own(tmp_path):
    script = "\nsol = Solution()\nassert sol.twoSum([3, 3], 6) == [0]\n"
    (tmp_path / "other.mu").write_text(TWO_SUM + script)
    run = session(tmp_path, "run", "other.mu")
    assert run.returncode == 1
    assert "Running from current.mu" not in run.stderr
    assert 'File "other.mu", line 10, in <module>' in run.stderr.replace(
        str(tmp_path) + "/", ""
    )
    assert "left : [0, 1]\nright: [0]" in run.stderr
    (tmp_path / "other.mu").write_text(TWO_SUM + script.replace("[0]", "[0, 1]"))
    assert session(tmp_path, "run", "other.mu").returncode == 0


def test_nothing_to_do_without_current_mu(tmp_path):
    shutil.copy(drill_for(reference("d115_")), tmp_path / "current.py")
    assert session(tmp_path, "fold").returncode == 0
    assert f"# mu {VERSION}" not in (tmp_path / "current.py").read_text()


PROBLEM = '''"""
URL: https://leetcode.com/problems/two-sum/description/

1. Two Sum

Given nums and target, return the indices of the two numbers that add up
to target.
"""


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        pass


sol = Solution()

# assert sol.twoSum([2, 7, 11, 15], 9) == [0, 1]
'''

TWO_SUM = """class Solution
  def twoSum(nums: [int], target: int) -> [int]
    seen = {}
    for >i, x in nums
      if target - x in seen
        return [seen[target - x], i]
      seen[x] = i
"""


def test_a_problem_is_served_run_submitted_and_folded(tmp_path):
    (tmp_path / "current.py").write_text(PROBLEM)
    assert "Wrote current.mu" in session(tmp_path, "stub").stdout
    work = (tmp_path / "current.mu").read_text()
    assert work.startswith("# URL: https://leetcode.com/problems/two-sum/")
    work = work.replace(
        "class Solution\n  def twoSum(nums: [int], target: int) -> [int]\n    pass\n",
        TWO_SUM,
    )
    work = work.replace("# assert", "assert")
    (tmp_path / "current.mu").write_text(work)
    assert session(tmp_path, "run").returncode == 0
    # make submit sends the transpiled copy while current.mu holds the work
    assert session(tmp_path, "build").stdout.strip() == ".mu_current.py"
    sent = (tmp_path / ".mu_current.py").read_text()
    assert "URL: https://leetcode.com/problems/two-sum/" in sent
    assert "seen[x] = i" in sent
    session(tmp_path, "fold")
    assert (
        f"# mu {VERSION}\n# class Solution\n#   def twoSum"
        in (tmp_path / "current.py").read_text()
    )
    # current.mu still holds the work until file, so a submit sends its copy
    assert session(tmp_path, "build").stdout.strip() == ".mu_current.py"
    session(tmp_path, "file")
    assert (tmp_path / "current.py").read_text() == ""
    assert (tmp_path / "current.mu").read_text().startswith(
        "# URL: https://leetcode.com/problems/two-sum/"
    )


def test_a_second_fold_replaces_the_first(tmp_path):
    """`make solved` folds before it submits; when the submit fails and
    current.mu is written again, the next fold keeps one quote and one
    copy of the code, the new one, and the notes once."""
    (tmp_path / "current.py").write_text(PROBLEM)
    session(tmp_path, "stub")
    work = (tmp_path / "current.mu").read_text()
    work = work.replace("# ---\n", "# ---\n# LEETCODE: Wrong Answer\n")
    work = work.replace(
        "class Solution\n  def twoSum(nums: [int], target: int) -> [int]\n    pass\n",
        TWO_SUM,
    )
    (tmp_path / "current.mu").write_text(work)
    session(tmp_path, "fold")
    (tmp_path / "current.mu").write_text(work.replace("seen[x] = i", "seen[x] = i  # again"))
    session(tmp_path, "fold")
    py = (tmp_path / "current.py").read_text()
    assert py.count(f"# mu {VERSION}\n") == 1
    assert py.count("\nclass Solution") == 1
    assert "seen[x] = i  # again" in py
    assert py.count("LEETCODE: Wrong Answer") == 1


def test_debug_writes_the_python_and_a_line_map(tmp_path):
    import json

    (tmp_path / "current.py").write_text(PROBLEM)
    session(tmp_path, "stub")
    # before any work, the debugger runs current.py itself
    assert session(tmp_path, "debug").stdout.strip() == "current.py"
    assert not (tmp_path / ".mu_current.map.json").exists()
    work = (tmp_path / "current.mu").read_text()
    work = work.replace(
        "class Solution\n  def twoSum(nums: [int], target: int) -> [int]\n    pass\n",
        TWO_SUM,
    )
    (tmp_path / "current.mu").write_text(work)
    assert session(tmp_path, "debug").stdout.strip() == ".mu_current.py"
    py = (tmp_path / ".mu_current.py").read_text().split("\n")
    m = json.loads((tmp_path / ".mu_current.map.json").read_text())
    assert m["file"] == "current.mu"
    mu = work.split("\n")
    seen = set()
    for py_line, mu_line in m["lines"].items():
        # every mapped python line comes from a mu line of code, in order
        assert py[int(py_line) - 1].strip()
        assert mu[mu_line - 1].strip() and not mu[mu_line - 1].startswith("#")
        seen.add(mu_line)
    assert mu.index("      seen[x] = i") + 1 in seen
    assert py.index("            seen[x] = i") + 1 in {int(k) for k in m["lines"]}
    assert m["lines"][str(py.index("            seen[x] = i") + 1)] == (
        mu.index("      seen[x] = i") + 1
    )
    session(tmp_path, "fold")
    session(tmp_path, "file")
    assert not (tmp_path / ".mu_current.map.json").exists()
    # the solve filed, current.py empty: current.mu still debugs on its own
    (tmp_path / "current.py").write_text("")
    (tmp_path / "current.mu").write_text(work)
    assert session(tmp_path, "debug").stdout.strip() == ".mu_current.py"
    m = json.loads((tmp_path / ".mu_current.map.json").read_text())
    assert m["file"] == "current.mu"
    py = (tmp_path / ".mu_current.py").read_text().split("\n")
    assert m["lines"][str(py.index("            seen[x] = i") + 1)] == (
        mu.index("      seen[x] = i") + 1
    )
    ran = python(tmp_path, ".mu_current.py")
    assert ran.returncode == 0, ran.stdout[-1500:] + ran.stderr[-1500:]
    # any other mu file, by path
    (tmp_path / "other.mu").write_text(TWO_SUM)
    assert session(tmp_path, "debug", "other.mu").stdout.strip() == ".mu_current.py"
    m = json.loads((tmp_path / ".mu_current.map.json").read_text())
    assert m["file"] == "other.mu"
    assert 2 in set(m["lines"].values())


def test_a_design_problem_and_a_given_class_are_written_as_classes(tmp_path):
    design = PROBLEM.replace("class Solution:", "class StockPrice(Base):").replace(
        "sol = Solution()", "sol = StockPrice()"
    )
    (tmp_path / "current.py").write_text(design)
    assert "Wrote current.mu" in session(tmp_path, "stub").stdout
    work = (tmp_path / "current.mu").read_text()
    assert "\nclass StockPrice extends Base\n  def twoSum(" in work
    assert "\nsol = StockPrice()\n" in work
    given = PROBLEM.replace(
        "sol = Solution()",
        "class Master:\n    def guess(self, w: str) -> int:\n        return 0\n\n\nsol = Solution()",
    )
    (tmp_path / "current.py").write_text(given)
    assert "Wrote current.mu" in session(tmp_path, "stub").stdout
    work = (tmp_path / "current.mu").read_text()
    assert (
        "\nclass Master\n  def guess(w: str) -> int\n    return 0\n\nsol = Solution()"
        in work
    )
    # above Solution, a class with a body is given and stays Python; one
    # whose body is `pass` is there to be written
    above = PROBLEM.replace(
        "class Solution:",
        "class Color(Flag):\n    red = auto()\n\n\nclass Node:\n    pass\n\n\nclass Solution:",
    )
    (tmp_path / "current.py").write_text(above)
    assert "Wrote current.mu" in session(tmp_path, "stub").stdout
    work = (tmp_path / "current.mu").read_text()
    assert "Color" not in work and "\nclass Node\n  pass\n\nclass Solution\n" in work


def test_a_problem_mu_cannot_write_is_left_to_current_py(tmp_path):
    # a method with a default argument: mu has no form for it
    given = PROBLEM.replace("target: int)", "target: int = 0)")
    (tmp_path / "current.py").write_text(given)
    out = session(tmp_path, "stub")
    assert out.returncode == 0 and "solve it in current.py" in out.stdout
    assert not (tmp_path / "current.mu").exists()


@pytest.mark.parametrize(
    "annotation, want",
    [
        ("Optional['Node']", "Node?"),
        ("'Optional[Node]'", "Node?"),
        ("TreeNode | None", "TreeNode?"),
    ],
)
def test_optional_annotations(annotation, want):
    from mulang import mu_type

    assert mu_type(__import__("ast").parse(annotation, mode="eval").body) == want


def test_the_stub_keeps_a_comment_written_in_the_solution_body():
    src = open(
        os.path.join(ROOT, "drills", "ll-pointer-reversal", "d184_reverse_k.py")
    ).read()
    text = stub(src)
    kept = "    # don't hunt him = him don't hunt\n    # try hunt = him\n    # don't try\n    pass\n"
    assert kept in text
    transpile(text)


def test_a_python_group_drill_gets_a_stub_and_the_stub_alone_runs_current_py(tmp_path):
    """A drill of the python group is served in mu like any other. While
    current.mu is still the stub as served, run runs current.py, so a
    drill mu has no word for (match, with, logging) is solved there."""
    drill = glob.glob(os.path.join(ROOT, "drills", "py-logging", "d203_*.py"))[0]
    (tmp_path / "current.py").write_text(open(drill).read())
    out = session(tmp_path, "stub")
    assert out.returncode == 0 and "Wrote current.mu" in out.stdout
    assert "\nclass Solution\n  def " in (tmp_path / "current.mu").read_text()
    run = session(tmp_path, "run")
    assert "Running from current.mu." not in run.stderr
    assert run.returncode == 0 and run.stdout == "None\n"  # the served print, as is
    work = (tmp_path / "current.mu").read_text().replace("    pass\n", "    1\n", 1)
    (tmp_path / "current.mu").write_text(work)
    assert "Running from current.mu." in session(tmp_path, "run").stderr
