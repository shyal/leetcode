from adj_utils import adjacency, indegrees, levels


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


from collections import deque  # noqa: E402


def test_levels_counts_the_level_each_item_was_pushed_at():
    G = {0: [1, 2], 1: [3], 2: [3], 3: []}
    q = deque([0])
    seen = {0}
    out = []
    for d, node in levels(q):
        out.append((d, node))
        for nxt in G[node]:
            if nxt not in seen:
                seen.add(nxt)
                q.append(nxt)
    assert out == [(0, 0), (1, 1), (1, 2), (2, 3)]


def test_levels_starts_every_seed_at_level_zero():
    q = deque([7, 8])
    out = list(levels(q))
    assert out == [(0, 7), (0, 8)]


def test_levels_grouped_yields_one_list_per_level():
    G = {0: [1, 2], 1: [3], 2: [3], 3: []}
    q = deque([0])
    seen = {0}
    out = []
    for d, level in levels(q, grouped=True):
        out.append((d, level))
        for node in level:
            for nxt in G[node]:
                if nxt not in seen:
                    seen.add(nxt)
                    q.append(nxt)
    assert out == [(0, [0]), (1, [1, 2]), (2, [3])]


def test_levels_empty_queue_yields_nothing():
    assert list(levels(deque())) == []


def test_levels_walk_parity_revisits_a_node_at_a_later_level():
    G = adjacency([[0, 1], [1, 2], [2, 3], [3, 1]], n=4)
    q = deque([(0, 0)])
    seen = {(0, 0)}
    ans = [-1] * 4
    for d, (node, parity) in levels(q):
        if parity == 0 and ans[node] == -1:
            ans[node] = d
        for nxt in G[node]:
            if (nxt, 1 - parity) not in seen:
                seen.add((nxt, 1 - parity))
                q.append((nxt, 1 - parity))
    assert ans == [0, 4, 2, 6]
