"""
DRILL: Alternating Cell
TRAINS: index-conversion

Given an integer n and an integer k, return the cell [r, c] that holds k
on an n x n grid. The grid is numbered 0 to n * n - 1 starting at the
bottom-left cell. The bottom row is filled left to right, the row above it
right to left, and the direction alternates on every row up. The cell
[r, c] is the r-th row from the top and the c-th column from the left,
both counted from 0.

Example 1:

Input: n = 4, k = 6
Output: [2, 1]
Explanation: the grid is numbered

    15 14 13 12
     8  9 10 11
     7  6  5  4
     0  1  2  3

and 6 sits in the third row from the top, second column.

Example 2:

Input: n = 4, k = 0
Output: [3, 0]

Example 3:

Input: n = 4, k = 15
Output: [0, 0]

Constraints:

    2 <= n <= 20
    0 <= k < n * n

    REQUIRED: O(1), arithmetic only. NO loop over cells, NO building the
    grid. The parity test is on the row counted from the bottom, not on
    r: testing r is the fail on an odd n.
"""


class Solution:

    def cell(self, n: int, k: int) -> List[int]:
        pass


sol = Solution()

print(sol.cell(4, 6))  # [2, 1]

# assert same_seq(sol.cell(4, 6), [2, 1])
# assert same_seq(sol.cell(4, 0), [3, 0])
# assert same_seq(sol.cell(4, 15), [0, 0])
# assert same_seq(sol.cell(4, 3), [3, 3])
# assert same_seq(sol.cell(4, 4), [2, 3])
# assert same_seq(sol.cell(4, 7), [2, 0])
# assert same_seq(sol.cell(4, 8), [1, 0])
# assert same_seq(sol.cell(4, 11), [1, 3])
# assert same_seq(sol.cell(4, 12), [0, 3])
# assert same_seq(sol.cell(3, 8), [0, 2])
# assert same_seq(sol.cell(3, 3), [1, 2])
# assert same_seq(sol.cell(5, 24), [0, 4])
# assert same_seq(sol.cell(5, 5), [3, 4])
# assert same_seq(sol.cell(6, 11), [4, 0])
# assert same_seq(sol.cell(6, 35), [0, 0])
# assert same_seq(sol.cell(20, 399), [0, 0])
# assert same_seq(sol.cell(20, 20), [18, 19])
