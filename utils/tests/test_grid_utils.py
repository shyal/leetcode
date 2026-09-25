from grid_utils import cells, edges, is_edge, like, nbrs, put, table


def test_cells_row_major():
    assert list(cells(table(2, 3))) == [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]


def test_cells_start_skips_row_zero_and_column_zero():
    assert list(cells(table(3, 3), start=1)) == [(1, 1), (1, 2), (2, 1), (2, 2)]


def test_cells_start_past_the_edge_is_empty():
    assert list(cells(table(2, 2), start=2)) == []


def test_cells_val_keeps_only_matching_cells():
    assert list(cells([[0, 1, 0], [1, 1, 0]], val=0)) == [(0, 0), (0, 2), (1, 2)]


def test_cells_val_combines_with_start():
    assert list(cells([[1, 1], [1, 1]], start=1, val=1)) == [(1, 1)]


def test_nbrs_val_keeps_only_matching_neighbours():
    assert list(nbrs([[0, 1, 0], [1, 0, 1]], 0, 1, val=0)) == [(0, 0), (0, 2), (1, 1)]


def test_put_writes_v_at_every_cell():
    grid = [[0, 1, 1], [1, 0, 0]]
    put(grid, cells(grid, val=1), 7)
    assert grid == [[0, 7, 7], [7, 0, 0]]


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


def test_is_edge_on_each_side_and_not_inside():
    g = table(3, 4)
    assert is_edge(g, 0, 2)
    assert is_edge(g, 2, 1)
    assert is_edge(g, 1, 0)
    assert is_edge(g, 1, 3)
    assert not is_edge(g, 1, 1)
    assert not is_edge(g, 1, 2)


def test_edges_lists_the_border_once_in_row_major_order():
    assert list(edges(table(3, 4))) == [
        (0, 0),
        (0, 1),
        (0, 2),
        (0, 3),
        (1, 0),
        (1, 3),
        (2, 0),
        (2, 1),
        (2, 2),
        (2, 3),
    ]


def test_edges_of_a_single_row_or_column_is_every_cell():
    assert list(edges(table(1, 3))) == [(0, 0), (0, 1), (0, 2)]
    assert list(edges(table(3, 1))) == [(0, 0), (1, 0), (2, 0)]
