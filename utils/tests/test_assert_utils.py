import pytest
from adj_utils import adjacency, indegrees
from assert_utils import same_rows, same_seq, uses


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
