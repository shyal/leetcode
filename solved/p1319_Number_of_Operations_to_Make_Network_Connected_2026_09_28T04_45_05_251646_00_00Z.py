"""
URL: https://leetcode.com/problems/number-of-operations-to-make-network-connected/description/?envType=problem-list-v2&envId=vn57k9wr

1319. Number of Operations to Make Network Connected

There are n computers numbered from 0 to n - 1 connected by ethernet cables connections forming a network where connections[i] = [a_i, b_i] represents a connection between computers a_i and b_i. Any computer can reach any other computer directly or indirectly through the network.

You are given an initial computer network connections. You can extract certain cables between two directly connected computers, and place them between any pair of disconnected computers to make them directly connected.

Return the minimum number of times you need to do this in order to make all the computers connected. If it is not possible, return -1.

Example 1:

Input: n = 4, connections = [[0,1],[0,2],[1,2]]
Output: 1
Explanation: Remove cable between computer 1 and 2 and place between computers 1 and 3.

Example 2:

Input: n = 6, connections = [[0,1],[0,2],[0,3],[1,2],[1,3]]
Output: 2

Example 3:

Input: n = 6, connections = [[0,1],[0,2],[0,3],[1,2]]
Output: -1
Explanation: There are not enough cables.

Constraints:

    1 <= n <= 10^5
    1 <= connections.length <= min(n * (n - 1) / 2, 10^5)
    connections[i].length == 2
    0 <= a_i, b_i < n
    a_i != b_i
    There are no repeated connections.
    No two computers are connected by more than one cable.
---
Got closer, but not close enough. Some mistakes, and not
seeing the num_groups - 1 answer
still learning

LEETCODE: Accepted (832 ms, 42.1 MB)
"""


# mu 0.6
# from dsa.union_find import UnionFind
#
# def makeConnected(n: int, connections: [[int]]) -> int
#   adj = adjacency(connections, n=n)
#   print(adj)
#   uf = UnionFind(n)
#   num_merged = sum for (a, b) in connections: int uf.union(a, b)
#   num_groups = len uf.groups()
#   num_cables = len connections
#   num_redundant = num_cables - num_merged
#   if num_redundant < num_groups - 1
#     return -1
#   num_groups - 1

from collections import defaultdict
from dsa.union_find import UnionFind


def adjacency(edges, n=None, reverse=False, directed=True, weighted=False):
    adj = defaultdict(dict) if weighted else defaultdict(list)
    for c in range(n or 0):
        adj[c]
    for e in edges:
        a, b = e[:2]
        if reverse:
            a, b = b, a
        if weighted:
            adj[a][b] = e[2]
            if not directed:
                adj[b][a] = e[2]
        else:
            adj[a].append(b)
            if not directed:
                adj[b].append(a)
    return adj


class Grid(list):
    """A list of rows that also takes a (row, col) pair as an index."""

    def __getitem__(self, k):
        if type(k) is tuple:
            return list.__getitem__(self, k[0])[k[1]]
        return list.__getitem__(self, k)

    def __setitem__(self, k, v):
        if type(k) is tuple:
            list.__getitem__(self, k[0])[k[1]] = v
        else:
            list.__setitem__(self, k, v)


class Solution:
    def makeConnected(self, n: int, connections: list[list[int]]) -> int:
        _in_connections, connections = connections, Grid(connections)
        _w_connections = connections
        try:
            adj = adjacency(connections, n=n)
            print(adj)
            uf = UnionFind(n)
            num_merged = sum(int(uf.union(a, b)) for (a, b) in connections)
            num_groups = len(uf.groups())
            num_cables = len(connections)
            num_redundant = num_cables - num_merged
            if num_redundant < num_groups - 1:
                return -1
            return num_groups - 1
        finally:
            _in_connections[:] = _w_connections


sol = Solution()
assert sol.makeConnected(6, [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3]]) == 2
