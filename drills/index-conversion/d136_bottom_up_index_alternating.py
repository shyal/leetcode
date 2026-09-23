"""
DRILL: Bottom Up Index Alternating
TRAINS: index-conversion

Given an integer n, return the n x n grid numbered 0 to n * n - 1,
starting at the bottom-left cell. The bottom row is filled left to
right, the row above it right to left, and the direction alternates on
every row up. The cell [r, c] is the r-th row from the top and the c-th
column from the left, both counted from 0.

Example 1:

Input: n = 4
Output: [[15, 14, 13, 12], [8, 9, 10, 11], [7, 6, 5, 4], [0, 1, 2, 3]]
Explanation: the grid is numbered

    15 14 13 12
     8  9 10 11
     7  6  5  4
     0  1  2  3

Example 2:

Input: n = 3
Output: [[6, 7, 8], [5, 4, 3], [0, 1, 2]]
Explanation: the grid is numbered

    6 7 8
    5 4 3
    0 1 2

Example 3:

Input: n = 2
Output: [[3, 2], [0, 1]]

Constraints:

    2 <= n <= 20

    REQUIRED: keep the stub's loop over the cells. Each cell gets its
    number by O(1) arithmetic on n, r and c. NO counter carried from one
    cell to the next. The parity test is on the row counted from the
    bottom, not on r: testing r is the fail on an odd n.
"""


class Solution:

    def numbered(self, n: int) -> List[List[int]]:
        grid = table(n, n)
        for r, c in cells(grid):
            pass
        return grid


sol = Solution()

print(sol.numbered(4))  # [[15, 14, 13, 12], [8, 9, 10, 11], [7, 6, 5, 4], [0, 1, 2, 3]]

# assert sol.numbered(4) == [[15, 14, 13, 12], [8, 9, 10, 11], [7, 6, 5, 4], [0, 1, 2, 3]]
# assert sol.numbered(3) == [[6, 7, 8], [5, 4, 3], [0, 1, 2]]
# assert sol.numbered(2) == [[3, 2], [0, 1]]
# assert sol.numbered(5) == [[20, 21, 22, 23, 24], [19, 18, 17, 16, 15], [10, 11, 12, 13, 14], [9, 8, 7, 6, 5], [0, 1, 2, 3, 4]]
# assert sol.numbered(6) == [[35, 34, 33, 32, 31, 30], [24, 25, 26, 27, 28, 29], [23, 22, 21, 20, 19, 18], [12, 13, 14, 15, 16, 17], [11, 10, 9, 8, 7, 6], [0, 1, 2, 3, 4, 5]]
# g = sol.numbered(20)
# assert g[0][0] == 399
# assert g[0][19] == 380
# assert g[19][0] == 0
# assert g[19][19] == 19
# assert g[1][0] == 360
# assert g[18][19] == 20
