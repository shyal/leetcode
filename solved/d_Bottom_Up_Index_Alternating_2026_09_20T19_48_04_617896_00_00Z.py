"""
DRILL: Bottom Up Index Alternating
TRAINS: index-conversion

Given an integer n and a cell [r, c] on an n x n grid, return the number
k that the cell holds. The grid is numbered 0 to n * n - 1 starting at
the bottom-left cell. The bottom row is filled left to right, the row
above it right to left, and the direction alternates on every row up.
The cell [r, c] is the r-th row from the top and the c-th column from
the left, both counted from 0.

Example 1:

Input: n = 4, r = 1, c = 2
Output: 10
Explanation: the grid is numbered

    15 14 13 12
     8  9 10 11
     7  6  5  4
     0  1  2  3

Example 2:

Input: n = 4, r = 3, c = 0
Output: 0

Example 3:

Input: n = 4, r = 0, c = 0
Output: 15

Constraints:

    2 <= n <= 20
    0 <= r, c < n

    REQUIRED: O(1), arithmetic only. NO loop over cells, NO building the
    grid. The parity test is on the row counted from the bottom, not on
    r: testing r is the fail on an odd n.

---

Learning

"""


class Solution:

    def index(self, n: int, r: int, c: int) -> int:
        return (n - r - 1) * n + (c if (n - r - 1) % 2 == 0 else n - c - 1)


sol = Solution()

print(sol.index(4, 1, 2))  # 10

assert sol.index(4, 1, 2) == 10
assert sol.index(4, 3, 0) == 0
assert sol.index(4, 0, 0) == 15
assert sol.index(4, 3, 3) == 3
assert sol.index(4, 2, 3) == 4
assert sol.index(4, 2, 1) == 6
assert sol.index(4, 2, 0) == 7
assert sol.index(4, 1, 0) == 8
assert sol.index(4, 1, 3) == 11
assert sol.index(4, 0, 3) == 12
assert sol.index(3, 0, 2) == 8
assert sol.index(3, 1, 2) == 3
assert sol.index(5, 0, 4) == 24
assert sol.index(5, 3, 4) == 5
assert sol.index(6, 4, 0) == 11
assert sol.index(20, 0, 0) == 399
assert sol.index(20, 18, 19) == 20
