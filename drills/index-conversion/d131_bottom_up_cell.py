"""
DRILL: Bottom Up Cell
TRAINS: index-conversion

Given an integer n and an integer k, return the cell [r, c] that holds k
on an n x n grid. The grid is numbered 0 to n * n - 1 starting at the
bottom-left cell. Each row is filled left to right, and each row is one
above the row before it. The cell [r, c] is the r-th row from the top and
the c-th column from the left, both counted from 0.

Example 1:

Input: n = 4, k = 6
Output: [2, 2]
Explanation: the grid is numbered

    12 13 14 15
     8  9 10 11
     4  5  6  7
     0  1  2  3

and 6 sits in the third row from the top, third column.

Example 2:

Input: n = 4, k = 0
Output: [3, 0]

Example 3:

Input: n = 4, k = 15
Output: [0, 3]

Constraints:

    2 <= n <= 20
    0 <= k < n * n

    REQUIRED: O(1), arithmetic only. NO loop over cells, NO building the
    grid.
"""


class Solution:

    def cell(self, n: int, k: int) -> List[int]:
        pass


sol = Solution()

print(sol.cell(4, 6))  # [2, 2]

# assert same_seq(sol.cell(4, 6), [2, 2])
# assert same_seq(sol.cell(4, 0), [3, 0])
# assert same_seq(sol.cell(4, 15), [0, 3])
# assert same_seq(sol.cell(4, 3), [3, 3])
# assert same_seq(sol.cell(4, 4), [2, 0])
# assert same_seq(sol.cell(4, 8), [1, 0])
# assert same_seq(sol.cell(4, 12), [0, 0])
# assert same_seq(sol.cell(2, 2), [0, 0])
# assert same_seq(sol.cell(5, 11), [2, 1])
# assert same_seq(sol.cell(20, 399), [0, 19])
# assert same_seq(sol.cell(20, 20), [18, 0])
