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


[1,0,1]
[0,0,0]
[1,0,1]

Ok so the idea here is a multibfs, with a res matrix,
we simple add the distance of each walk from the origin.

for 0,0 res becomes:

0 1 0
1 2 3
0 3 0

But that's not right.. because we need the max distance from each 1,

so all the distances need to be maximized.

Which means that every time we write into the res matrix, we actually
have to take the min of the distance from the originating cell.

This means that if we're at distance 0 from a 1, the res cell becomes zero.

But the 1 1 res cell never hits 0 or 1, so is the max.


"""


class Solution:
    def maxDistance(self, grid: List[List[int]]) -> int:
        def bfs(i, j):
            q = deque([[i, j, 0]])
            visited = set([])
            while q:
                ii, jj, dist = q.popleft()
                if (ii, jj) in visited:
                    continue
                visited.add((ii, jj))

                if grid[ii][jj] != 1:
                    res[ii][jj] = min(res[ii][jj], dist)

                if ii > 0:
                    q.append([ii - 1, jj, dist + 1])
                if ii < len(grid) - 1:
                    q.append([ii + 1, jj, dist + 1])
                if jj > 0:
                    q.append([ii, jj - 1, dist + 1])
                if jj < len(grid[0]) - 1:
                    q.append([ii, jj + 1, dist + 1])

        res = []
        for i in range(len(grid)):
            res.append([float("inf")] * len(grid[0]))

        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 1:
                    bfs(i, j)

        # tabulate(res)

        best = -1
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if res[i][j] != float("inf"):
                    best = max(res[i][j], best)

        return best


sol = Solution()

print(sol.maxDistance([[1, 0, 1], [0, 0, 0], [1, 0, 1]]))  # 2

assert sol.maxDistance([[1, 0, 1], [0, 0, 0], [1, 0, 1]]) == 2
assert sol.maxDistance([[1, 0, 0], [0, 0, 0], [0, 0, 0]]) == 4
assert sol.maxDistance([[1]]) == -1
assert sol.maxDistance([[0]]) == -1
assert sol.maxDistance([[1, 1], [1, 1]]) == -1
assert sol.maxDistance([[0, 0], [0, 0]]) == -1

assert sol.maxDistance([[1, 0], [0, 0]]) == 2
assert sol.maxDistance([[0, 1], [0, 0]]) == 2
assert sol.maxDistance([[0, 0, 0], [0, 1, 0], [0, 0, 0]]) == 2
assert sol.maxDistance([[1] + [0] * 99] + [[0] * 100 for _ in range(99)]) == 198
assert sol.maxDistance([[0] * 99 + [1]] + [[0] * 100 for _ in range(99)]) == 198
assert sol.maxDistance([[1] * 50 + [0] * 50] + [[0] * 100 for _ in range(99)]) == 149
assert sol.maxDistance([[0] * 100 for _ in range(100)]) == -1
assert (
    sol.maxDistance(
        [[1 if (i + j) % 2 == 0 else 0 for j in range(10)] for i in range(10)]
    )
    == 1
)
assert sol.maxDistance([[0, 1, 0], [1, 0, 1], [0, 1, 0]]) == 1
assert (
    sol.maxDistance(
        [
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
        ]
    )
    == 4
)
assert sol.maxDistance([[1] + [0] * 9] + [[0] * 10 for _ in range(9)]) == 18
