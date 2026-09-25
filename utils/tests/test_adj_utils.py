from adj_utils import adjacency, indegrees, levels
from grid_utils import cells, nbrs, table


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


def test_levels_seen_drops_an_item_popped_twice():
    q = deque([1, 1, 2])
    seen: set = set()
    assert list(levels(q, seen=seen)) == [(0, 1), (0, 2)]
    assert seen == {1, 2}


def test_levels_grid_gte_drops_cells_below_the_bound():
    grid = [[3, 1, 2], [3, 0, 2], [3, 3, 3]]
    q = deque([(0, 0)])
    seen: set = set()
    for _, (r, c) in levels(q, grid, seen, gte=3):
        q.extend(nbrs(grid, r, c))
    assert seen == {(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)}


def test_levels_checks_the_first_item_too():
    q = deque([(0, 0)])
    seen: set = set()
    assert list(levels(q, [[1, 5], [5, 5]], seen, gte=2)) == []
    assert seen == set()


def test_levels_d_is_the_shortest_distance_with_duplicates_in_q():
    grid = table(3, 3)
    q = deque([(0, 0)])
    dist = {}
    for d, (r, c) in levels(q, grid, set()):
        dist[(r, c)] = d
        q.extend(nbrs(grid, r, c))
    assert dist == {(i, j): i + j for i, j in cells(grid)}


def test_levels_without_grid_compares_the_item_itself():
    assert list(levels(deque([1, 5, 2]), lt=3)) == [(0, 1), (0, 2)]


def test_levels_grouped_drops_filtered_items_and_empty_levels():
    q = deque([1, 1, 7])
    assert list(levels(q, seen=set(), grouped=True, lt=5)) == [(0, [1])]
