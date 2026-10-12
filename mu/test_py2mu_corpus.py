"""py2mu on the cached problems: the translation of each passes its asserts."""

import os
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
os.environ.setdefault("MU_CACHE", os.path.join(ROOT, ".prepare_cache"))
sys.path.insert(0, HERE)
import leetmu  # noqa: E402, F401
from mulang.py2mu import one  # noqa: E402


@pytest.mark.parametrize("num", [200, 322, 875, 1143, 2812])
def test_cached_problem_passes_its_asserts(num):
    row = one(num)
    assert row["status"] == "pass", row.get("why")
    assert row["mu_lines"] <= row["py_lines"]  # the class line counts on both sides
