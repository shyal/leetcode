import json

import assert_utils
import pytest
from assert_utils import same_rows, same_seq, tle, uses
from pydsa.adj import adjacency, indegrees


def test_same_rows_ignores_order_inside_a_row():
    assert same_rows([[3, 0], [1]], [[0, 3], [1]])


def test_same_rows_accepts_sets_against_lists():
    assert same_rows([{2}, {0, 3}], [[2], [3, 0]])


def test_same_rows_keeps_row_order():
    assert not same_rows([[1], [2]], [[2], [1]])


def test_same_rows_lengths_must_match():
    assert not same_rows([[1]], [[1], []])
    assert same_rows([], [])


class Uses:
    def f(self, edges):
        return adjacency(edges)


def test_uses_passes_when_every_helper_is_called():
    assert uses(Uses, adjacency)


def test_uses_names_the_helper_the_class_never_calls():
    with pytest.raises(AssertionError, match="Uses never calls indegrees"):
        uses(Uses, adjacency, indegrees)


def test_same_seq_tuple_against_list():
    assert same_seq((1, 2), [1, 2])
    assert same_seq([1, 2], (1, 2))


def test_same_seq_keeps_order():
    assert not same_seq((1, 2), [2, 1])
    assert not same_seq((1,), [1, 2])


def _tle_case(tmp_path, monkeypatch, seconds):
    monkeypatch.setattr(assert_utils, "_CACHE", str(tmp_path))
    (tmp_path / "9.tle.json").write_text(
        json.dumps({"args": [[1, 2, 3]], "expected": [True, False], "seconds": seconds})
    )


def test_tle_passes_the_reference_answer_in_time(tmp_path, monkeypatch):
    _tle_case(tmp_path, monkeypatch, 1.0)
    assert tle(lambda xs: [True, False], 9)


def test_tle_names_the_first_answer_that_differs(tmp_path, monkeypatch):
    _tle_case(tmp_path, monkeypatch, 1.0)
    with pytest.raises(
        AssertionError, match=r"9: wrong answer .* answer 1 is True, expected False"
    ):
        tle(lambda xs: [True, True], 9)
    with pytest.raises(AssertionError, match="1 answers, expected 2"):
        tle(lambda xs: [True], 9)


def test_tle_fails_a_call_slower_than_the_slack_allows(tmp_path, monkeypatch):
    _tle_case(tmp_path, monkeypatch, 1e-9)
    with pytest.raises(
        AssertionError,
        match=r"9: .* s on the case that timed out on leetcode, 0.00 s allowed",
    ):
        tle(lambda xs: [True, False] + sorted(range(10**5))[:0], 9)
