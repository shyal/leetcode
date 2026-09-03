"""
URL: https://leetcode.com/problems/as-far-from-land-as-possible/description/?envType=problem-list-v2&envId=vn57k9wr

1162. As Far from Land as Possible

Given an n x n grid containing only values 0 and 1, where 0 represents water and 1 represents land, find a water cell such that its distance to the nearest land cell is maximized, and return the distance. If no land or water exists in the grid, return -1.

The distance used in this problem is the Manhattan distance: the distance between two cells (x0, y0) and (x1, y1) is |x0 - x1| + |y0 - y1|.

Example 1:

Input: grid = [[1,0,1],[0,0,0],[1,0,1]]
Output: 2
Explanation: The cell (1, 1) is as far as possible from all the land with distance 2.

Example 2:

Input: grid = [[1,0,0],[0,0,0],[0,0,0]]
Output: 4
Explanation: The cell (2, 2) is as far as possible from all the land with distance 4.

Constraints:

    n == grid.length
    n == grid[i].length
    1 <= n <= 100
    grid[i][j] is 0 or 1

---

Probably not the most efficient solution... need to revisit.

"""


class Solution:
    def maxDistance(self, grid: List[List[int]]) -> int:
        def bfs(cell):
            q = deque([(cell, 0)])
            visited = {cell}
            while q:
                node, dist = q.popleft()
                row, col = node
                if grid[row][col] != 1:
                    wdist[row][col] = dist

                neigh = []

                if row > 0:
                    neigh.append((row - 1, col))
                if row < len(grid) - 1:
                    neigh.append((row + 1, col))
                if col > 0:
                    neigh.append((row, col - 1))
                if col < len(grid[0]) - 1:
                    neigh.append((row, col + 1))

                for nxt in neigh:
                    if nxt not in visited:
                        visited.add(nxt)
                        q.append((nxt, dist + 1))
            return -1

        dists = []

        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j]:
                    wdist = [[0] * len(grid[0]) for _ in range(len(grid))]
                    bfs((i, j))
                    dists.append(wdist)

        vals = []
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                v = []
                for d in dists:
                    v.append(d[i][j])
                if len(set(v)) == 1 and v[0] != 0:
                    vals.append(v[0])

        if vals:
            return max(vals)
        return -1


sol = Solution()

# print(sol.maxDistance([[1, 0, 1], [0, 0, 0], [1, 0, 1]]))  # 2

assert sol.maxDistance([[1, 0, 1], [0, 0, 0], [1, 0, 1]]) == 2
print(sol.maxDistance([[1, 0, 0], [0, 0, 0], [0, 0, 0]]))
assert sol.maxDistance([[1]]) == -1
assert sol.maxDistance([[0]]) == -1
assert sol.maxDistance([[1, 1], [1, 1]]) == -1
assert sol.maxDistance([[0, 0], [0, 0]]) == -1

assert sol.maxDistance([[1, 0], [0, 0]]) == 2
assert sol.maxDistance([[0, 1], [0, 0]]) == 2
assert sol.maxDistance([[0, 0, 0], [0, 1, 0], [0, 0, 0]]) == 2
assert sol.maxDistance([[1] + [0] * 99] + [[0] * 100 for _ in range(99)]) == 198
assert sol.maxDistance([[0] * 99 + [1]] + [[0] * 100 for _ in range(99)]) == 198
# assert sol.maxDistance([[1] * 50 + [0] * 50] + [[0] * 100 for _ in range(99)]) == 149
# assert sol.maxDistance([[0] * 100 for _ in range(100)]) == -1
# assert sol.maxDistance([[1] * 100 for _ in range(100)]) == -1
# assert (
#     sol.maxDistance(
#         [[1 if (i + j) % 2 == 0 else 0 for j in range(10)] for i in range(10)]
#     )
#     == 1
# )
# assert sol.maxDistance([[0, 1, 0], [1, 0, 1], [0, 1, 0]]) == 1
# assert (
#     sol.maxDistance(
#         [
#             [0, 0, 0, 0, 1],
#             [0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0],
#             [1, 0, 0, 0, 0],
#         ]
#     )
#     == 4
# )
# assert sol.maxDistance([[1] + [0] * 9] + [[0] * 10 for _ in range(9)]) == 18
