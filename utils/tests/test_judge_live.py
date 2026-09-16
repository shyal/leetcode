# The live judge: one real model call per case, opt-in because it needs a
# key and the network. `make test-judge` runs it; `make check` skips it.
# Each case is a real solve file from solved/ whose verdict once came out
# wrong, and the assertion is the rule that fixed the prompt. DeepSeek is
# the default judge and a call costs a fraction of a cent, so add a case
# whenever a verdict is corrected by hand.
import json
import os
import subprocess

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
KG_EXTRACT = os.path.join(ROOT, "utils", "rs", "target", "release", "kg_extract")

pytestmark = pytest.mark.skipif(
    os.environ.get("KG_LIVE_JUDGE") != "1",
    reason="live model call; run with KG_LIVE_JUDGE=1 (make test-judge)",
)


def judge(path: str) -> dict:
    out = subprocess.run(
        [KG_EXTRACT, "--file", path, "--dry", "--model", "deepseek"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
        timeout=300,
    ).stdout
    # the verdict, then the run's "Done:" line
    verdict, _ = json.JSONDecoder().raw_decode(out, out.index("{"))
    return verdict


def test_tle_blames_the_missing_move_not_the_brute_force():
    # 974 on 2026-09-16: a prefix-sum brute force over every (i, j) pair,
    # rejected with Time Limit Exceeded. The pair loop ran correctly; the
    # move that was missing is the remainder count.
    verdict = judge(
        "solved/p974_Subarray_Sums_Divisible_by_K_2026_09_16T03_59_41_528332_00_00Z.py"
    )
    moves = verdict["moves"]
    assert moves.get("substring-enumeration", "clean") == "clean", moves
    assert moves.get("prefix-sum-hashmap") == "struggled", moves
    assert "Time Limit Exceeded" in verdict.get("note", ""), verdict
