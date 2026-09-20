"""
DRILL: Top Down Index
TRAINS: index-conversion

Given an integer n and a cell [r, c] on an n x n grid, return the number
k that the cell holds. The grid is numbered 0 to n * n - 1 starting at
the top-left cell. Each row is filled left to right, and each row is one
below the row before it. The cell [r, c] is the r-th row from the top
and the c-th column from the left, both counted from 0.

Example 1:

Input: n = 4, r = 1, c = 2
Output: 6
Explanation: the grid is numbered

     0  1  2  3
     4  5  6  7
     8  9 10 11
    12 13 14 15

Example 2:

Input: n = 4, r = 0, c = 0
Output: 0

Example 3:

Input: n = 4, r = 3, c = 3
Output: 15

Constraints:

    2 <= n <= 20
    0 <= r, c < n

    REQUIRED: O(1), arithmetic only. NO loop over cells, NO building the
    grid.
"""


class Solution:

    def index(self, n: int, r: int, c: int) -> int:
        return r * n + c


sol = Solution()

print(sol.index(4, 1, 2))  # 6

assert sol.index(4, 1, 2) == 6
assert sol.index(4, 0, 0) == 0
assert sol.index(4, 3, 3) == 15
assert sol.index(4, 0, 3) == 3
assert sol.index(4, 1, 0) == 4
assert sol.index(4, 2, 3) == 11
assert sol.index(4, 3, 0) == 12
assert sol.index(2, 1, 0) == 2
assert sol.index(5, 2, 1) == 11
assert sol.index(20, 19, 19) == 399
assert sol.index(20, 1, 0) == 20
