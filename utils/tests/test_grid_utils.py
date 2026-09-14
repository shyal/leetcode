from grid_utils import cells, table


def test_cells_row_major():
    assert list(cells(table(2, 3))) == [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]


def test_cells_start_skips_row_zero_and_column_zero():
    assert list(cells(table(3, 3), start=1)) == [(1, 1), (1, 2), (2, 1), (2, 2)]


def test_cells_start_past_the_edge_is_empty():
    assert list(cells(table(2, 2), start=2)) == []
