"""
DRILL: Alternating Cell
TRAINS: index-conversion

Given an integer n and an integer k, return the cell [r, c] that holds k
on an n x n grid. The grid is numbered 1 to n * n starting at the
bottom-left cell. The bottom row is filled left to right, the row above it
right to left, and the direction alternates on every row up. The cell
[r, c] is the r-th row from the top and the c-th column from the left,
both counted from 0.

Example 1:

Input: n = 4, k = 6
Output: [2, 2]
Explanation: the grid is numbered

    16 15 14 13
     9 10 11 12
     8  7  6  5
     1  2  3  4

and 6 sits in the third row from the top, third column.

Example 2:

Input: n = 4, k = 1
Output: [3, 0]

Example 3:

Input: n = 4, k = 16
Output: [0, 0]

Constraints:

    2 <= n <= 20
    1 <= k <= n * n

    REQUIRED: O(1), arithmetic only. NO loop over cells, NO building the
    grid. The parity test is on the row counted from the bottom, not on
    r: testing r is the fail on an odd n.
"""


class Solution:

    def cell(self, n: int, k: int) -> List[int]:
        pass


sol = Solution()

print(sol.cell(4, 6))  # [2, 2]

# assert same_seq(sol.cell(4, 6), [2, 2])
# assert same_seq(sol.cell(4, 1), [3, 0])
# assert same_seq(sol.cell(4, 16), [0, 0])
# assert same_seq(sol.cell(4, 4), [3, 3])
# assert same_seq(sol.cell(4, 5), [2, 3])
# assert same_seq(sol.cell(4, 8), [2, 0])
# assert same_seq(sol.cell(4, 9), [1, 0])
# assert same_seq(sol.cell(4, 12), [1, 3])
# assert same_seq(sol.cell(4, 13), [0, 3])
# assert same_seq(sol.cell(3, 9), [0, 2])
# assert same_seq(sol.cell(3, 4), [1, 2])
# assert same_seq(sol.cell(5, 25), [0, 4])
# assert same_seq(sol.cell(5, 6), [3, 4])
# assert same_seq(sol.cell(6, 12), [4, 0])
# assert same_seq(sol.cell(6, 36), [0, 0])
# assert same_seq(sol.cell(20, 400), [0, 0])
# assert same_seq(sol.cell(20, 21), [18, 19])
