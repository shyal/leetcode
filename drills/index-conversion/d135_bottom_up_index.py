"""
DRILL: Bottom Up Index
TRAINS: index-conversion

Given an integer n, return the n x n grid numbered 0 to n * n - 1,
starting at the bottom-left cell. Each row is filled left to right, and
each row is one above the row before it. The cell [r, c] is the r-th row
from the top and the c-th column from the left, both counted from 0.

Example 1:

Input: n = 4
Output: [[12, 13, 14, 15], [8, 9, 10, 11], [4, 5, 6, 7], [0, 1, 2, 3]]
Explanation: the grid is numbered

    12 13 14 15
     8  9 10 11
     4  5  6  7
     0  1  2  3

Example 2:

Input: n = 3
Output: [[6, 7, 8], [3, 4, 5], [0, 1, 2]]
Explanation: the grid is numbered

    6 7 8
    3 4 5
    0 1 2

Example 3:

Input: n = 2
Output: [[2, 3], [0, 1]]

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

print(sol.numbered(4))  # [[12, 13, 14, 15], [8, 9, 10, 11], [4, 5, 6, 7], [0, 1, 2, 3]]

# assert sol.numbered(4) == [[12, 13, 14, 15], [8, 9, 10, 11], [4, 5, 6, 7], [0, 1, 2, 3]]
# assert sol.numbered(3) == [[6, 7, 8], [3, 4, 5], [0, 1, 2]]
# assert sol.numbered(2) == [[2, 3], [0, 1]]
# assert sol.numbered(5) == [[20, 21, 22, 23, 24], [15, 16, 17, 18, 19], [10, 11, 12, 13, 14], [5, 6, 7, 8, 9], [0, 1, 2, 3, 4]]
# assert sol.numbered(6) == [[30, 31, 32, 33, 34, 35], [24, 25, 26, 27, 28, 29], [18, 19, 20, 21, 22, 23], [12, 13, 14, 15, 16, 17], [6, 7, 8, 9, 10, 11], [0, 1, 2, 3, 4, 5]]
# g = sol.numbered(20)
# assert g[0][0] == 380
# assert g[0][19] == 399
# assert g[19][0] == 0
# assert g[19][19] == 19
# assert g[1][0] == 360
# assert g[18][19] == 39
