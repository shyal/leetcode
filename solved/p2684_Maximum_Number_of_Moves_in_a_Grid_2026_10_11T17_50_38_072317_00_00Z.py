"""
URL: https://leetcode.com/problems/maximum-number-of-moves-in-a-grid/description/?envType=problem-list-v2&envId=vn57k9wr

2684. Maximum Number of Moves in a Grid

You are given a 0-indexed m x n matrix grid consisting of positive integers.

You can start at any cell in the first column of the matrix, and traverse the grid in the following way:

- From a cell (row, col), you can move to any of the cells: (row - 1, col + 1), (row, col + 1) and (row + 1, col + 1) such that the value of the cell you move to, should be strictly bigger than the value of the current cell.

Return the maximum number of moves that you can perform.

Example 1:

Input: grid = [[2,4,3,5],[5,4,9,3],[3,4,2,11],[10,9,13,15]]
Output: 3
Explanation: We can start at the cell (0, 0) and make the following moves:
- (0, 0) -> (0, 1).
- (0, 1) -> (1, 2).
- (1, 2) -> (2, 3).
It can be shown that it is the maximum number of moves that can be made.

Example 2:

Input: grid = [[3,2,4],[2,1,9],[1,1,7]]
Output: 0
Explanation: Starting from any cell in the first column we cannot perform any moves.

Constraints:

    m == grid.length
    n == grid[i].length
    2 <= m, n <= 1000
    4 <= m * n <= 10^5
    1 <= grid[i][j] <= 10^6

---

LEETCODE: Accepted (423 ms, 59.9 MB)
"""


# mu 0.8
# class Solution
#   def maxMoves(grid: [[int]]) -> int
#     memo helper(row, col)
#       moves = []
#       for (ni, nj) in [(row - 1, col + 1), (row, col + 1), (row + 1, col + 1)]
#         if in_bounds(grid, ni, nj) and grid[ni][nj] > grid[row][col]
#           moves <- helper(ni, nj)
#       max(moves, default=0) + (1 if moves else 0)
#     max([helper(r, 0) for r in 0..<len(grid)])

from functools import cache
import sys
import threading


sys.setrecursionlimit(1 << 20)


def deep(fn):
    """Run fn on a thread with a 256 MB stack, so deep memo recursion fits."""
    out, err = [], []

    def target():
        try:
            out.append(fn())
        except BaseException as e:
            err.append(e)

    threading.stack_size(1 << 28)
    t = threading.Thread(target=target)
    t.start()
    t.join()
    if err:
        raise err[0]
    return out[0]


def in_bounds(grid, r, c=None):
    if c is None:
        r, c = r
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])


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
    def maxMoves(self, grid: list[list[int]]) -> int:
        _in_grid, grid = grid, Grid(grid)
        _w_grid = grid
        try:
            def run():
                @cache
                def helper(row, col):
                    moves = []
                    for (ni, nj) in [(row - 1, col + 1), (row, col + 1), (row + 1, col + 1)]:
                        if in_bounds(grid, ni, nj) and grid[ni][nj] > grid[row][col]:
                            moves.append(helper(ni, nj))
                    return max(moves, default=0) + (1 if moves else 0)
                return max([helper(r, 0) for r in range(0, len(grid))])
            return deep(run)
        finally:
            _in_grid[:] = _w_grid


sol = Solution()
print(sol.maxMoves([[2, 4, 3, 5], [5, 4, 9, 3], [3, 4, 2, 11], [10, 9, 13, 15]]))
_l, _r = sol.maxMoves([[2, 4, 3, 5], [5, 4, 9, 3], [3, 4, 2, 11], [10, 9, 13, 15]]), 3
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxMoves([[3, 2, 4], [2, 1, 9], [1, 1, 7]]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxMoves([[1, 2]]), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxMoves([[1], [2]]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxMoves([[1, 1, 1, 1]]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxMoves([[1], [1], [1], [1]]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxMoves([[1, 2, 3, 4, 5]]), 4
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxMoves([[5, 4, 3, 2, 1]]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxMoves([[1, 2], [2, 3], [3, 4], [4, 5]]), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxMoves([[5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5]]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxMoves([[1] * 1000 for _ in range(0, 100)]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxMoves([[i for i in range(0, 1000)] for _ in range(0, 100)]), 999
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxMoves([[10 ** 6 - j for j in range(0, 1000)] for _ in range(0, 100)]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxMoves([[1, 1000000] * 500]), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
