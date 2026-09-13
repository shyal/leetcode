"""
DRILL: Neighbour Counts

Given a grid of m rows and n columns, return a table of the same shape
where each cell holds the number of cardinal neighbours of that cell that
lie on the grid. Use like, cells and nbrs from the harness.

Example 1:

Input: grid = [[1, 0, 2], [0, 1, 0]]
Output: [[2, 3, 2], [2, 3, 2]]

Example 2:

Input: grid = [[1]]
Output: [[0]]

Example 3:

Input: grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
Output: [[2, 3, 2], [3, 4, 3], [2, 3, 2]]

Constraints:

    1 <= m, n <= 1000

    REQUIRED: O(mn). NO rows that share one list, NO if per offset.
"""


class Solution:
    def neighbour_counts(self, grid: list[list[int]]) -> list[list[int]]:
        res = like(grid)
        for i, j in cells(grid):
            res[i][j] = len([*nbrs(grid, i, j)])
        return res


sol = Solution()

print(sol.neighbour_counts([[1, 0, 2], [0, 1, 0]]))  # [[2, 3, 2], [2, 3, 2]]

assert sol.neighbour_counts([[1, 0, 2], [0, 1, 0]]) == [[2, 3, 2], [2, 3, 2]]
assert sol.neighbour_counts([[1]]) == [[0]]
assert sol.neighbour_counts([[0, 0, 0], [0, 0, 0], [0, 0, 0]]) == [
    [2, 3, 2],
    [3, 4, 3],
    [2, 3, 2],
]
assert sol.neighbour_counts([[0, 0, 0, 0]]) == [[1, 2, 2, 1]]
assert sol.neighbour_counts([[0], [0], [0]]) == [[1], [2], [1]]
t = sol.neighbour_counts([[0, 0], [0, 0]])
t[0][0] = 9
assert t == [[9, 2], [2, 2]]
