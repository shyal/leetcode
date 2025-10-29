"""
URL: https://leetcode.com/problems/projection-area-of-3d-shapes/description/?envType=problem-list-v2&envId=vn57k9wr

883. Projection Area of 3D Shapes

You are given an n x n grid where we place some 1 x 1 x 1 cubes that are axis-aligned with the x, y, and z axes.

Each value v = grid[i][j] represents a tower of v cubes placed on top of the cell (i, j).

We view the projection of these cubes onto the xy, yz, and zx planes.

A projection is like a shadow, that maps our 3-dimensional figure to a 2-dimensional plane. We are viewing the "shadow" when looking at the cubes from the top, the front, and the side.

Return the total area of all three projections.

Example 1:

Input: grid = [[1,2],[3,4]]
Output: 17
Explanation: Here are the three projections ("shadows") of the shape made with each axis-aligned plane.

Example 2:

Input: grid = [[2]]
Output: 5

Example 3:

Input: grid = [[1,0],[0,2]]
Output: 8

Constraints:

    n == grid.length == grid[i].length
    1 <= n <= 50
    0 <= grid[i][j] <= 50
"""


class Solution:
    def projectionArea(self, grid: List[List[int]]) -> int:
        if not grid:
            return 0
        if not grid[0]:
            return 0
        col = lambda i: [grid[x][i] for x in range(len(grid))]
        z = sum(x != 0 for x in chain(*grid))
        y = sum(max(row) for row in grid)
        x = sum(max(col(c)) for c in range(len(next(iter(grid), []))))
        return x + y + z


sol = Solution()

assert sol.projectionArea([[1, 2], [3, 4]]) == 17
assert sol.projectionArea([[2]]) == 5
assert sol.projectionArea([[1, 0], [0, 2]]) == 8
assert sol.projectionArea([[0]]) == 0
assert sol.projectionArea([[1]]) == 3
assert sol.projectionArea([[0, 0], [0, 0]]) == 0
assert sol.projectionArea([[50]]) == 101
assert sol.projectionArea([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == 51
assert sol.projectionArea([[1, 0, 3], [0, 0, 0], [7, 0, 9]]) == 32
assert sol.projectionArea([[0, 1], [2, 0]]) == 8
assert sol.projectionArea([]) == 0
assert sol.projectionArea([[]]) == 0
