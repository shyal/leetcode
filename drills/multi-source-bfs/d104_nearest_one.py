"""
DRILL: Nearest One

Given a grid of m rows and n columns holding only 0 and 1, with at least
one 1, return a table of the same shape where each cell holds the number
of cardinal steps from that cell to the nearest 1. Use grid_bfs from the
harness.

Example 1:

Input: grid = [[1, 0, 0], [0, 1, 0]]
Output: [[0, 1, 2], [1, 0, 1]]

Example 2:

Input: grid = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
Output: [[2, 1, 2], [1, 0, 1], [2, 1, 2]]

Example 3:

Input: grid = [[1, 0], [0, 0], [0, 0], [0, 0]]
Output: [[0, 1], [1, 2], [2, 3], [3, 4]]

Constraints:

    1 <= m, n <= 1000
    grid[i][j] is 0 or 1
    at least one cell is 1

    REQUIRED: O(mn), one queue seeded with every 1. NO BFS per cell.
"""


class Solution:
    def nearest_one(self, grid: list[list[int]]) -> list[list[int]]:
        pass


sol = Solution()

print(sol.nearest_one([[1, 0, 0], [0, 1, 0]]))  # [[0, 1, 2], [1, 0, 1]]

# assert sol.nearest_one([[1, 0, 0], [0, 1, 0]]) == [[0, 1, 2], [1, 0, 1]]
# assert sol.nearest_one([[0, 0, 0], [0, 1, 0], [0, 0, 0]]) == [[2, 1, 2], [1, 0, 1], [2, 1, 2]]
# assert sol.nearest_one([[1, 0], [0, 0], [0, 0], [0, 0]]) == [[0, 1], [1, 2], [2, 3], [3, 4]]
# assert sol.nearest_one([[1]]) == [[0]]
# assert sol.nearest_one([[0, 0, 0, 1]]) == [[3, 2, 1, 0]]
# assert sol.nearest_one([[1, 1], [1, 1]]) == [[0, 0], [0, 0]]
# assert sol.nearest_one([[1] + [0] * 999] + [[0] * 1000 for _ in range(999)])[999][999] == 1998
