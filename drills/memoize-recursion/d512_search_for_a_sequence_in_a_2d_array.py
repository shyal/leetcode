"""
EPI 16.5 Search for a sequence in a 2D array

Given a grid of integers and a list pattern, return True when the grid
holds pattern along a walk of cells, and False otherwise. A walk starts
at any cell, and each next cell shares a side with the cell before it.
The k-th cell of the walk holds pattern[k]. A walk may visit a cell
more than once. An empty pattern is always held.

Example 1:

Input: grid = [[1, 2, 3],
               [3, 4, 5],
               [5, 6, 7]], pattern = [1, 3, 4, 6]
Output: True
Explanation: (0, 0) holds 1, (1, 0) holds 3, (1, 1) holds 4 and (2, 1)
holds 6.

Example 2:

Input: grid = [[1, 2, 3],
               [3, 4, 5],
               [5, 6, 7]], pattern = [1, 2, 3, 4]
Output: False
Explanation: the only 3 next to the 2 is at (0, 2), and no 4 is next
to it.

Example 3:

Input: grid = [[1, 2],
               [3, 4]], pattern = [1, 2, 1, 2]
Output: True
Explanation: the walk goes (0, 0), (0, 1), (0, 0), (0, 1).

Constraints:

    1 <= len(grid), len(grid[0]) <= 50
    0 <= len(pattern) <= 200
    0 <= grid[i][j], pattern[k] <= 100

    REQUIRED: O(len(grid) * len(grid[0]) * len(pattern)) time. NO
    search that tries the same cell for the same position of pattern
    more than once.
"""


class Solution:
    def is_pattern_contained_in_grid(self, grid: list[list[int]], pattern: list[int]) -> bool:
        pass


sol = Solution()

print(sol.is_pattern_contained_in_grid([[1, 2, 3], [3, 4, 5], [5, 6, 7]], [1, 3, 4, 6]))  # True

# G = [[1, 2, 3], [3, 4, 5], [5, 6, 7]]
# assert sol.is_pattern_contained_in_grid(G, [1, 3, 4, 6]) is True
# assert sol.is_pattern_contained_in_grid(G, [1, 2, 3, 4]) is False
# assert sol.is_pattern_contained_in_grid([[1, 2], [3, 4]], [1, 2, 1, 2]) is True
# assert sol.is_pattern_contained_in_grid(G, []) is True
# assert sol.is_pattern_contained_in_grid(G, [7]) is True
# assert sol.is_pattern_contained_in_grid(G, [8]) is False
# assert sol.is_pattern_contained_in_grid(G, [1, 5]) is False
# assert sol.is_pattern_contained_in_grid([[1, 2], [3, 4]], [1, 4]) is False
# assert sol.is_pattern_contained_in_grid([[5]], [5, 5]) is False
# assert sol.is_pattern_contained_in_grid([[5]], [5]) is True
# assert sol.is_pattern_contained_in_grid(G, [5, 6, 7, 5]) is True
# assert sol.is_pattern_contained_in_grid(G, [3, 4, 5, 7, 6, 5]) is True
# ones = [[1] * 50 for _ in range(50)]
# assert sol.is_pattern_contained_in_grid(ones, [1] * 199 + [2]) is False
# corner = [[1] * 50 for _ in range(50)]
# corner[49][49] = 2
# assert sol.is_pattern_contained_in_grid(corner, [1] * 150 + [2]) is True
# assert sol.is_pattern_contained_in_grid(corner, [2, 1, 2, 1, 2]) is True
# assert sol.is_pattern_contained_in_grid(corner, [2, 2]) is False
