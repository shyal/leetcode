"""
DRILL: Count Cells

Given a grid of m rows and n columns and an integer v, return the number
of cells of grid equal to v. Use cells from the harness.

Example 1:

Input: grid = [[1, 0, 2], [0, 1, 0]], v = 0
Output: 3

Example 2:

Input: grid = [[1, 0, 2], [0, 1, 0]], v = 5
Output: 0

Constraints:

    1 <= m, n <= 1000
    -10**9 <= grid[i][j], v <= 10**9

    REQUIRED: O(mn). NO nested range loops.
"""


class Solution:
    def count(self, grid: list[list[int]], v: int) -> int:
        count = 0
        for i, j in cells(grid):
            if grid[i][j] == v:
                count += 1
        return count


sol = Solution()

print(sol.count([[1, 0, 2], [0, 1, 0]], 0))  # 3

assert sol.count([[1, 0, 2], [0, 1, 0]], 0) == 3
assert sol.count([[1, 0, 2], [0, 1, 0]], 5) == 0
assert sol.count([[7]], 7) == 1
assert sol.count([[2, 2, 2, 2]], 2) == 4
assert sol.count([[3], [3], [1]], 3) == 2
assert sol.count([[0] * 1000 for _ in range(1000)], 0) == 1000000
