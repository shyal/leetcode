"""
DRILL: Top Down Index
TRAINS: index-conversion

Given an integer n, return the n x n grid numbered 0 to n * n - 1,
starting at the top-left cell. Each row is filled left to right, and
each row is one below the row before it. The cell [r, c] is the r-th row
from the top and the c-th column from the left, both counted from 0.

Example 1:

Input: n = 4
Output: [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
Explanation: the grid is numbered

     0  1  2  3
     4  5  6  7
     8  9 10 11
    12 13 14 15

Example 2:

Input: n = 3
Output: [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
Explanation: the grid is numbered

    0 1 2
    3 4 5
    6 7 8

Example 3:

Input: n = 2
Output: [[0, 1], [2, 3]]

Constraints:

    2 <= n <= 20

    REQUIRED: keep the stub's loop over the cells. Each cell gets its
    number by O(1) arithmetic on n, r and c. NO counter carried from one
    cell to the next.
"""


class Solution:

    def numbered(self, n: int) -> List[List[int]]:
        grid = table(n, n)
        for r, c in cells(grid):
            pass
        return grid


sol = Solution()

print(sol.numbered(4))  # [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]

# assert sol.numbered(4) == [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
# assert sol.numbered(3) == [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
# assert sol.numbered(2) == [[0, 1], [2, 3]]
# assert sol.numbered(5) == [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19], [20, 21, 22, 23, 24]]
# assert sol.numbered(6) == [[0, 1, 2, 3, 4, 5], [6, 7, 8, 9, 10, 11], [12, 13, 14, 15, 16, 17], [18, 19, 20, 21, 22, 23], [24, 25, 26, 27, 28, 29], [30, 31, 32, 33, 34, 35]]
# g = sol.numbered(20)
# assert g[0][0] == 0
# assert g[0][19] == 19
# assert g[19][0] == 380
# assert g[19][19] == 399
# assert g[1][0] == 20
# assert g[18][19] == 379
