"""
URL: https://leetcode.com/problems/most-stones-removed-with-same-row-or-column/description/?envType=problem-list-v2&envId=vn57k9wr

947. Most Stones Removed with Same Row or Column

On a 2D plane, we place n stones at some integer coordinate points. Each coordinate point may have at most one stone.

A stone can be removed if it shares either the same row or the same column as another stone that has not been removed.

Given an array stones of length n where stones[i] = [x_i, y_i] represents the location of the i-th stone, return the largest possible number of stones that can be removed.

Example 1:

Input: stones = [[0,0],[0,1],[1,0],[1,2],[2,1],[2,2]]
Output: 5
Explanation: One way to remove 5 stones is as follows:
1. Remove stone [2,2] because it shares the same row as [2,1].
2. Remove stone [2,1] because it shares the same column as [0,1].
3. Remove stone [1,2] because it shares the same row as [1,0].
4. Remove stone [1,0] because it shares the same column as [0,0].
5. Remove stone [0,1] because it shares the same row as [0,0].
Stone [0,0] cannot be removed since it does not share a row/column with another stone still on the plane.

Example 2:

Input: stones = [[0,0],[0,2],[1,1],[2,0],[2,2]]
Output: 3
Explanation: One way to make 3 moves is as follows:
1. Remove stone [2,2] because it shares the same row as [2,0].
2. Remove stone [2,0] because it shares the same column as [0,0].
3. Remove stone [0,2] because it shares the same row as [0,0].
Stones [0,0] and [1,1] cannot be removed since they do not share a row/column with another stone still on the plane.

Example 3:

Input: stones = [[0,0]]
Output: 0
Explanation: [0,0] is the only stone on the plane, so you cannot remove it.

Constraints:

    1 <= stones.length <= 1000
    0 <= x_i, y_i <= 10^4
    No two stones are at the same coordinate point.
---
Learning

LEETCODE: Accepted (39 ms, 22.5 MB)
"""


# mu 0.6
# def removeStones(stones: [[int]]) -> int
#   rk = x -> f"r{x}"
#   ck = x -> f"c{x}"
#
#   parent = {}
#   for (r, c) in stones
#     parent[rk(r)] = rk(r)
#     parent[ck(c)] = ck(c)
#
#   def find(x)
#     if parent[x] != x
#       parent[x] = find(parent[x])
#     return parent[x]
#
#   def union(a, b)
#     pa, pb = find(a), find(b)
#     if pa != pb
#       parent[pa] = pb
#
#   for (a, b) in stones
#     union(rk(a), ck(b))
#
#   # draw_graphviz(parent, type='directed')
#
#   groups = sum(1 for k in parent if k == find(k))
#   return len(stones) - groups

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
    def removeStones(self, stones: list[list[int]]) -> int:
        _in_stones, stones = stones, Grid(stones)
        _w_stones = stones
        try:
            rk = lambda x: f"r{x}"
            ck = lambda x: f"c{x}"
            parent = {}
            for (r, c) in stones:
                parent[rk(r)] = rk(r)
                parent[ck(c)] = ck(c)
            def find(x):
                if parent[x] != x:
                    parent[x] = find(parent[x])
                return parent[x]
            def union(a, b):
                pa, pb = find(a), find(b)
                if pa != pb:
                    parent[pa] = pb
            for (a, b) in stones:
                union(rk(a), ck(b))
            groups = sum(1 for k in parent if k == find(k))
            return len(stones) - groups
        finally:
            _in_stones[:] = _w_stones


sol = Solution()
print(sol.removeStones([[0, 0], [0, 1], [1, 0], [1, 2], [2, 1], [2, 2]]))
assert sol.removeStones([[0, 0], [0, 1], [1, 0], [1, 2], [2, 1], [2, 2]]) == 5
assert sol.removeStones([[0, 0], [0, 2], [1, 1], [2, 0], [2, 2]]) == 3
assert sol.removeStones([[0, 0]]) == 0
assert sol.removeStones([[0, 0], [0, 0]]) == 1
assert sol.removeStones([[0, 0], [0, 1], [0, 2], [0, 3], [0, 4]]) == 4
assert sol.removeStones([[0, 0], [1, 0], [2, 0], [3, 0], [4, 0]]) == 4
assert sol.removeStones([[0, 0], [1, 1], [2, 2], [3, 3], [4, 4]]) == 0
assert sol.removeStones([[0, 0], [-1, 0], [-2, 0], [-3, 0], [-4, 0]]) == 4
assert sol.removeStones([[0, 0], [0, 10000], [10000, 0], [10000, 10000]]) == 3
assert sol.removeStones([[i, i] for i in range(0, 1000)]) == 0
assert sol.removeStones([[i, 0] for i in range(0, 1000)]) == 999
assert sol.removeStones([[i, i % 2] for i in range(0, 1000)]) == 998
assert sol.removeStones([[0, 0], [0, 1], [1, 0], [1, 1], [2, 2], [2, 3], [3, 2], [3, 3]]) == 6
assert sol.removeStones([[0, 0], [0, 1], [1, 0], [1, 1], [2, 2], [2, 3], [3, 2], [3, 3], [4, 4]]) == 6
