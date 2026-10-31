"""mu/chrome, the Chrome extension: the ratings it shows are the repo's
(kg_rs.solve_ratings through build.py), and the line map behind the
errors LeetCode reports (submit.origin)."""

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
CHROME = ROOT / "mu" / "chrome"


# --- ratings -----------------------------------------------------------------


def write_tables(root, zerotrac, clist, meta):
    data = root / "data"
    data.mkdir()
    (data / "leetcode_ratings.tsv").write_text(
        "rating\tid\tslug\n"
        + "".join(f"{r}\t{num}\t{slug}\n" for num, slug, r in zerotrac)
    )
    (data / "clist_problems.json").write_text(
        json.dumps([{"slug": s, "rating": r} for s, r in clist])
    )
    (data / "problems_metadata.json").write_text(
        json.dumps({num: {"slug": slug} for num, slug in meta})
    )


def test_kg_rs_solve_ratings_is_zerotrac_then_rescaled_clist(tmp_path):
    import kg_rs

    # the two problems both tables rate fix the line: CLIST 1000 -> 1200,
    # 2000 -> 2400, so slope 1.2 and intercept 0; problem 3, CLIST only,
    # lands at 1800; problem 4, zerotrac only, keeps zerotrac's number
    write_tables(
        tmp_path,
        zerotrac=[("1", "a", 1200.0), ("2", "b", 2400.0), ("4", "d", 1555.5)],
        clist=[("a", 1000), ("b", 2000), ("c", 1500)],
        meta=[("1", "a"), ("2", "b"), ("3", "c"), ("4", "d")],
    )
    r = kg_rs.solve_ratings(str(tmp_path))
    assert r["1"] == 1200.0 and r["2"] == 2400.0 and r["4"] == 1555.5
    assert r["3"] == pytest.approx(1800.0)
    assert set(r) == {"1", "2", "3", "4"}


def test_build_problem_ratings_maps_slugs_and_rounds(tmp_path, monkeypatch):
    # build.py runs on import: load just its function through its source
    src = (CHROME / "build.py").read_text()
    body = src[
        src.index("def problem_ratings") : src.index("shutil.copy(mulang.__file__")
    ]
    import kg_rs

    ns: dict = {"json": json, "kg_rs": kg_rs}
    exec(body, ns)  # noqa: S102 - the repo's own file
    problem_ratings = ns["problem_ratings"]
    write_tables(
        tmp_path,
        zerotrac=[("1", "a", 1200.4), ("2", "b", 2400.0)],
        clist=[("a", 1000), ("b", 2000), ("c", 1500)],
        meta=[("1", "a"), ("2", "b"), ("3", "c")],
    )
    assert problem_ratings(tmp_path) == {"a": 1200, "b": 2400, "c": 1800}


def test_ratings_json_is_slug_to_one_number():
    path = CHROME / "ratings.json"
    if not path.exists():
        pytest.skip("make mu-chrome has not run")
    ratings = json.loads(path.read_text())
    assert ratings and all(isinstance(v, int) for v in ratings.values())


# --- the line map ------------------------------------------------------------


@pytest.fixture
def submit():
    sys.path.insert(0, str(CHROME.parent))  # session.py beside the chrome folder
    try:
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "chrome_submit", CHROME / "submit.py"
        )
        assert spec and spec.loader
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    finally:
        sys.path.pop(0)


# solved/d_Count_Smaller_Values_2026_10_26: a helper pasted (table), a
# loop, a branch, an implicit return
MU = """class Solution
  def smallerThanEach(nums: [int]) -> [int]
    buckets = table(101)
    for v in nums
      buckets[v] += 1
    res = {:int}
    count = 0
    for >i, v in buckets
      if v
        res[i] = count
      count += v
    [res[v] for v in nums]
"""


def test_origin_has_one_entry_per_submission_line(submit):
    sub = submit.submission(MU)
    origin = json.loads(submit.origin(MU))
    assert len(origin) == len(sub.splitlines())


def test_origin_header_is_unmapped_and_python_lines_point_at_their_mu(submit):
    sub = submit.submission(MU).splitlines()
    origin = json.loads(submit.origin(MU))
    head = 1 + len(MU.strip("\n").splitlines()) + 1
    assert origin[:head] == [None] * head

    def mu_line_of(start):
        (k,) = [k for k, line in enumerate(sub) if line.strip().startswith(start)]
        return origin[k]

    assert mu_line_of("for v in nums") == 4
    assert mu_line_of("if v") == 9
    assert mu_line_of("return [res[v]") == 12
    # the pasted helper's own lines are nobody's mu line
    assert mu_line_of("def table(") is None
