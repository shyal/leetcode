from adj_utils import adjacency, indegrees


def test_indegrees_counts_the_head_of_each_edge():
    assert indegrees([[0, 1], [0, 2], [1, 2]], 3, type=list) == [0, 1, 2]


def test_indegrees_reverse_reads_each_edge_backwards():
    assert indegrees([[0, 1], [0, 2]], 3, reverse=True, type=list) == [2, 0, 0]


def test_indegrees_undirected_counts_both_ends():
    assert indegrees([[0, 1], [0, 2]], 3, directed=False, type=list) == [2, 1, 1]
    deg = indegrees([[3, 4]], directed=False)
    assert (deg[3], deg[4], deg[9]) == (1, 1, 0)


def test_adjacency_undirected_lists_both_ends():
    assert adjacency([[0, 1]], 3, directed=False) == {0: [1], 1: [0], 2: []}
