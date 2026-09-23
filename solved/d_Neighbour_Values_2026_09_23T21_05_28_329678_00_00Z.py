"""
DRILL: Neighbour Values

Given a grid of m rows and n columns and a cell (r, c), return the values
of the cardinal neighbours of (r, c) that lie on the grid, in the order
up, left, right, down. Use nbrs from the harness.

Example 1:

Input: grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]], r = 1, c = 1
Output: [2, 4, 6, 8]

Example 2:

Input: grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]], r = 0, c = 0
Output: [2, 4]
Explanation: (-1, 0) and (0, -1) are off the grid.

Example 3:

Input: grid = [[1]], r = 0, c = 0
Output: []

Constraints:

    1 <= m, n <= 1000
    0 <= r < m
    0 <= c < n

    REQUIRED: one pass over the four offsets. NO if per offset, NO
    try/except around an index.
"""


class Solution:
    @as_list
    def neighbour_values(self, grid: list[list[int]], r: int, c: int) -> list[int]:
        return (grid[i][j] for i, j in nbrs(grid, r, c))


sol = Solution()

print(sol.neighbour_values([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 1, 1))  # [2, 4, 6, 8]

assert sol.neighbour_values([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 1, 1) == [2, 4, 6, 8]
assert sol.neighbour_values([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 0, 0) == [2, 4]
assert sol.neighbour_values([[1]], 0, 0) == []
assert sol.neighbour_values([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 2, 2) == [6, 8]
assert sol.neighbour_values([[1, 2, 3, 4]], 0, 2) == [2, 4]
assert sol.neighbour_values([[1], [2], [3], [4]], 2, 0) == [2, 4]
