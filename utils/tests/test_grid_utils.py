from grid_utils import cells, edges, is_edge, like, nbrs, put, shape, table


def test_cells_row_major():
    assert list(cells(table(2, 3))) == [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]


def test_cells_start_skips_row_zero_and_column_zero():
    assert list(cells(table(3, 3), start=1)) == [(1, 1), (1, 2), (2, 1), (2, 2)]


def test_cells_start_past_the_edge_is_empty():
    assert list(cells(table(2, 2), start=2)) == []


def test_cells_eq_keeps_only_matching_cells():
    assert list(cells([[0, 1, 0], [1, 1, 0]], eq=0)) == [(0, 0), (0, 2), (1, 2)]


def test_cells_val_is_the_old_name_for_eq():
    assert list(cells([[0, 1, 0], [1, 1, 0]], val=0)) == [(0, 0), (0, 2), (1, 2)]


def test_cells_eq_combines_with_start():
    assert list(cells([[1, 1], [1, 1]], start=1, eq=1)) == [(1, 1)]


def test_cells_lt_lte_gt_gte_compare_each_value():
    grid = [[1, 2, 3], [4, 5, 6]]
    assert list(cells(grid, lt=3)) == [(0, 0), (0, 1)]
    assert list(cells(grid, lte=3)) == [(0, 0), (0, 1), (0, 2)]
    assert list(cells(grid, gt=5)) == [(1, 2)]
    assert list(cells(grid, gte=5)) == [(1, 1), (1, 2)]


def test_cells_comparisons_combine_with_and():
    assert list(cells([[1, 2, 3], [4, 5, 6]], gte=2, lt=5)) == [(0, 1), (0, 2), (1, 0)]


def test_cells_zero_bound_is_still_tested():
    assert list(cells([[-1, 0, 1]], gte=0)) == [(0, 1), (0, 2)]


def test_nbrs_eq_keeps_only_matching_neighbours():
    assert list(nbrs([[0, 1, 0], [1, 0, 1]], 0, 1, eq=0)) == [(0, 0), (0, 2), (1, 1)]


def test_nbrs_gte_drops_neighbours_below_the_bound():
    assert list(nbrs([[3, 1, 2], [3, 0, 2]], 0, 1, gte=2)) == [(0, 0), (0, 2)]


def test_put_writes_v_at_every_cell():
    grid = [[0, 1, 1], [1, 0, 0]]
    put(grid, cells(grid, eq=1), 7)
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


def test_shape_follows_nested_lists_down():
    assert shape([[3, 1, 2], [3, 0, 2]]) == (2, 3)
    assert shape(table(2, 3, 4)) == (2, 3, 4)
    assert shape([5, 6, 7]) == (3,)


def test_shape_stops_at_a_tuple_cell_and_at_an_empty_row():
    assert shape([[(0, 1), (2, 3)]]) == (1, 2)
    assert shape([[]]) == (1, 0)
    assert shape([]) == (0,)


def test_shape_of_several_sequences_is_one_size_each():
    assert shape("abcde", "ace") == (5, 3)


def test_shape_last_index_is_every_size_less_one():
    assert shape([[3, 1, 2], [3, 0, 2], [3, 3, 3]], last_index=True) == (2, 2)
    assert shape("abcde", "ace", last_index=True) == (4, 2)
