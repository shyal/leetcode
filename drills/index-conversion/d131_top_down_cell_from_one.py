"""
DRILL: Top Down Cell From One
TRAINS: index-conversion

Given an integer n and an integer k, return the cell [r, c] that holds k
on an n x n grid. The grid is numbered 1 to n * n starting at the
top-left cell. Each row is filled left to right, and each row is one
below the row before it. The cell [r, c] is the r-th row from the top and
the c-th column from the left, both counted from 0.

Example 1:

Input: n = 4, k = 6
Output: [1, 1]
Explanation: the grid is numbered

     1  2  3  4
     5  6  7  8
     9 10 11 12
    13 14 15 16

and 6 sits in the second row, second column.

Example 2:

Input: n = 4, k = 1
Output: [0, 0]

Example 3:

Input: n = 4, k = 16
Output: [3, 3]

Constraints:

    2 <= n <= 20
    1 <= k <= n * n

    REQUIRED: O(1), arithmetic only. NO loop over cells, NO building the
    grid. The off-by-one is the fail: k starts at 1, r and c start at 0.
"""


class Solution:

    def cell(self, n: int, k: int) -> List[int]:
        pass


sol = Solution()

print(sol.cell(4, 6))  # [1, 1]

# assert same_seq(sol.cell(4, 6), [1, 1])
# assert same_seq(sol.cell(4, 1), [0, 0])
# assert same_seq(sol.cell(4, 16), [3, 3])
# assert same_seq(sol.cell(4, 4), [0, 3])
# assert same_seq(sol.cell(4, 5), [1, 0])
# assert same_seq(sol.cell(4, 12), [2, 3])
# assert same_seq(sol.cell(4, 13), [3, 0])
# assert same_seq(sol.cell(2, 3), [1, 0])
# assert same_seq(sol.cell(5, 12), [2, 1])
# assert same_seq(sol.cell(20, 400), [19, 19])
# assert same_seq(sol.cell(20, 21), [1, 0])
