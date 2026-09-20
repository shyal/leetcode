"""
DRILL: Bottom Up Index
TRAINS: index-conversion

Given an integer n and a cell [r, c] on an n x n grid, return the number
k that the cell holds. The grid is numbered 0 to n * n - 1 starting at
the bottom-left cell. Each row is filled left to right, and each row is
one above the row before it. The cell [r, c] is the r-th row from the
top and the c-th column from the left, both counted from 0.

Example 1:

Input: n = 4, r = 1, c = 2
Output: 10
Explanation: the grid is numbered

    12 13 14 15
     8  9 10 11
     4  5  6  7
     0  1  2  3

Example 2:

Input: n = 4, r = 3, c = 0
Output: 0

Example 3:

Input: n = 4, r = 0, c = 3
Output: 15

Constraints:

    2 <= n <= 20
    0 <= r, c < n

    REQUIRED: O(1), arithmetic only. NO loop over cells, NO building the
    grid.
"""


class Solution:

    def index(self, n: int, r: int, c: int) -> int:
        pass


sol = Solution()

print(sol.index(4, 1, 2))  # 10

# assert sol.index(4, 1, 2) == 10
# assert sol.index(4, 3, 0) == 0
# assert sol.index(4, 0, 3) == 15
# assert sol.index(4, 3, 3) == 3
# assert sol.index(4, 2, 0) == 4
# assert sol.index(4, 1, 0) == 8
# assert sol.index(4, 0, 0) == 12
# assert sol.index(2, 0, 0) == 2
# assert sol.index(5, 2, 1) == 11
# assert sol.index(20, 0, 19) == 399
# assert sol.index(20, 18, 0) == 20
