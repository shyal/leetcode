"""
DRILL: Top Down Index Alternating
TRAINS: index-conversion

Given an integer n and a cell [r, c] on an n x n grid, return the number
k that the cell holds. The grid is numbered 0 to n * n - 1 starting at
the top-left cell. The top row is filled left to right, the row below it
right to left, and the direction alternates on every row down. The cell
[r, c] is the r-th row from the top and the c-th column from the left,
both counted from 0.

Example 1:

Input: n = 4, r = 1, c = 2
Output: 5
Explanation: the grid is numbered

     0  1  2  3
     7  6  5  4
     8  9 10 11
    15 14 13 12

Example 2:

Input: n = 4, r = 0, c = 0
Output: 0

Example 3:

Input: n = 4, r = 3, c = 0
Output: 15

Constraints:

    2 <= n <= 20
    0 <= r, c < n

    REQUIRED: O(1), arithmetic only. NO loop over cells, NO building the
    grid. The parity test is on r: the top row is even.
"""


class Solution:

    def index(self, n: int, r: int, c: int) -> int:
        return r * n + (c if r % 2 == 0 else (n - 1) - c)


sol = Solution()

print(sol.index(4, 1, 2))  # 5

assert sol.index(4, 1, 2) == 5
assert sol.index(4, 0, 0) == 0
assert sol.index(4, 3, 0) == 15
assert sol.index(4, 0, 3) == 3
assert sol.index(4, 1, 3) == 4
assert sol.index(4, 1, 0) == 7
assert sol.index(4, 2, 0) == 8
assert sol.index(4, 2, 3) == 11
assert sol.index(4, 3, 3) == 12
assert sol.index(3, 2, 2) == 8
assert sol.index(3, 1, 0) == 5
assert sol.index(5, 4, 4) == 24
assert sol.index(5, 3, 4) == 15
assert sol.index(20, 19, 0) == 399
assert sol.index(20, 1, 19) == 20
