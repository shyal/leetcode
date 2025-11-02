"""
URL: https://leetcode.com/problems/count-unguarded-cells-in-the-grid/description/?envType=problem-list-v2&envId=vn57k9wr

2257. Count Unguarded Cells in the Grid

You are given two integers m and n representing a 0-indexed m x n grid. You are also given two 2D integer arrays guards and walls where guards[i] = [row_i, col_i] and walls[j] = [row_j, col_j] represent the positions of the i-th guard and j-th wall respectively.

A guard can see every cell in the four cardinal directions (north, east, south, or west) starting from their position unless obstructed by a wall or another guard. A cell is guarded if there is at least one guard that can see it.

Return the number of unoccupied cells that are not guarded.

Example 1:

Input: m = 4, n = 6, guards = [[0,0],[1,1],[2,3]], walls = [[0,1],[2,2],[1,4]]
Output: 7
Explanation: The guarded and unguarded cells are shown in red and green respectively in the above diagram.
There are a total of 7 unguarded cells, so we return 7.

Example 2:

Input: m = 3, n = 3, guards = [[1,1]], walls = [[0,1],[1,0],[2,1],[1,2]]
Output: 4
Explanation: The unguarded cells are shown in green in the above diagram.
There are a total of 4 unguarded cells, so we return 4.

Constraints:

    1 <= m, n <= 10^5
    2 <= m * n <= 10^5
    1 <= guards.length, walls.length <= 5 * 10^4
    2 <= guards.length + walls.length <= m * n
    guards[i].length == walls[j].length == 2
    0 <= row_i, row_j < m
    0 <= col_i, col_j < n
    All the positions in guards and walls are unique.

---

Interesting.. using a defaultdict lead to a TLE, but using a 2d array didn't.

That's a big difference in performance.

"""


class Solution:
    def countUnguarded(
        self, m: int, n: int, guards: List[List[int]], walls: List[List[int]]
    ) -> int:

        class Cardinals:
            north = 0
            south = 1
            east = 2
            west = 3

        grid = []
        for _ in range(m):
            grid.append(["."] * n)
        for grow, gcol in guards:
            grid[grow][gcol] = "g"

        for grow, gcol in walls:
            grid[grow][gcol] = "w"

        for grow, gcol in guards:
            for cardinal in [
                Cardinals.north,
                Cardinals.south,
                Cardinals.east,
                Cardinals.west,
            ]:
                if cardinal == Cardinals.north:
                    for i in range(grow - 1, -1, -1):
                        if grid[i][gcol] == "w" or grid[i][gcol] == "g":
                            break
                        grid[i][gcol] = "x"
                if cardinal == Cardinals.south:
                    for i in range(grow + 1, m):
                        if grid[i][gcol] == "w" or grid[i][gcol] == "g":
                            break
                        grid[i][gcol] = "x"
                if cardinal == Cardinals.east:
                    for i in range(gcol + 1, n):
                        if grid[grow][i] == "w" or grid[grow][i] == "g":
                            break
                        grid[grow][i] = "x"
                if cardinal == Cardinals.west:
                    for i in range(gcol - 1, -1, -1):
                        if grid[grow][i] == "w" or grid[grow][i] == "g":
                            break
                        grid[grow][i] = "x"
        unguarded = sum(x.count(".") for x in grid)
        return unguarded


sol = Solution()

# print(sol.countUnguarded(4, 6, [[0, 0], [1, 1], [2, 3]], [[0, 1], [2, 2], [1, 4]]))  # 7

assert sol.countUnguarded(4, 6, [[0, 0], [1, 1], [2, 3]], [[0, 1], [2, 2], [1, 4]]) == 7
assert sol.countUnguarded(3, 3, [[1, 1]], [[0, 1], [1, 0], [2, 1], [1, 2]]) == 4
assert sol.countUnguarded(1, 3, [[0, 0]], [[0, 1]]) == 1
assert sol.countUnguarded(1, 3, [[0, 0]], [[0, 2]]) == 0
assert sol.countUnguarded(2, 2, [[0, 0]], [[0, 1]]) == 1
assert sol.countUnguarded(1, 2, [[0, 0]], [[0, 1]]) == 0
assert sol.countUnguarded(3, 3, [[0, 0]], [[0, 1]]) == 5
assert sol.countUnguarded(1, 5, [[0, 4]], [[0, 1], [0, 3]]) == 2
assert sol.countUnguarded(1, 4, [[0, 0], [0, 3]], [[0, 1]]) == 0
assert sol.countUnguarded(2, 2, [[0, 0]], [[1, 0], [1, 1]]) == 0
import json

with open("misc/test_data/2257.json") as r:
    TLE = json.loads(r.read())

assert sol.countUnguarded(100_000, 1, TLE, [[81215, 0]]) == 0
