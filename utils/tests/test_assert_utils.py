from assert_utils import same_rows


def test_same_rows_ignores_order_inside_a_row():
    assert same_rows([[3, 0], [1]], [[0, 3], [1]])


def test_same_rows_accepts_sets_against_lists():
    assert same_rows([{2}, {0, 3}], [[2], [3, 0]])


def test_same_rows_keeps_row_order():
    assert not same_rows([[1], [2]], [[2], [1]])


def test_same_rows_lengths_must_match():
    assert not same_rows([[1]], [[1], []])
    assert same_rows([], [])
