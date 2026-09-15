from grid_utils import cells, like, table


def test_cells_row_major():
    assert list(cells(table(2, 3))) == [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]


def test_cells_start_skips_row_zero_and_column_zero():
    assert list(cells(table(3, 3), start=1)) == [(1, 1), (1, 2), (2, 1), (2, 2)]


def test_cells_start_past_the_edge_is_empty():
    assert list(cells(table(2, 2), start=2)) == []


def test_table_one_dimension_is_a_flat_list():
    assert table(4) == [0, 0, 0, 0]
    assert table(3, fill=float("inf")) == [float("inf")] * 3


def test_table_two_dimensions_has_distinct_rows():
    t = table(2, 3, fill=1)
    assert t == [[1, 1, 1], [1, 1, 1]]
    t[0][0] = 9
    assert t[1][0] == 1


def test_table_three_dimensions_nests():
    assert table(2, 1, 2) == [[[0, 0]], [[0, 0]]]


def test_like_copies_the_shape_only():
    assert like([[1, 2, 3], [4, 5, 6]], fill=-1) == [[-1, -1, -1], [-1, -1, -1]]
