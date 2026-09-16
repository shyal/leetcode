"""
URL: https://leetcode.com/problems/find-the-safest-path-in-a-grid/description/?envType=problem-list-v2&envId=vn57k9wr

2812. Find the Safest Path in a Grid

You are given a 0-indexed 2D matrix grid of size n x n, where (r, c) represents:
- A cell containing a thief if grid[r][c] = 1
- An empty cell if grid[r][c] = 0

You are initially positioned at cell (0, 0). In one move, you can move to any adjacent cell in the grid, including cells containing thieves.

The safeness factor of a path on the grid is defined as the minimum manhattan distance from any cell in the path to any thief in the grid.

Return the maximum safeness factor of all paths leading to cell (n - 1, n - 1).

An adjacent cell of cell (r, c), is one of the cells (r, c + 1), (r, c - 1), (r + 1, c) and (r - 1, c) if it exists.

The Manhattan distance between two cells (a, b) and (x, y) is equal to |a - x| + |b - y|, where |val| denotes the absolute value of val.

Example 1:

Input: grid = [[1,0,0],[0,0,0],[0,0,1]]
Output: 0
Explanation: All paths from (0, 0) to (n - 1, n - 1) go through the thieves in cells (0, 0) and (n - 1, n - 1).

Example 2:

Input: grid = [[0,0,1],[0,0,0],[0,0,0]]
Output: 2
Explanation: The path depicted in the picture above has a safeness factor of 2 since:
- The closest cell of the path to the thief at cell (0, 2) is cell (0, 0). The distance between them is | 0 - 0 | + | 0 - 2 | = 2.
It can be shown that there are no other paths with a higher safeness factor.

Example 3:

Input: grid = [[0,0,0,1],[0,0,0,0],[0,0,0,0],[1,0,0,0]]
Output: 2
Explanation: The path depicted in the picture above has a safeness factor of 2 since:
- The closest cell of the path to the thief at cell (0, 3) is cell (1, 2). The distance between them is | 0 - 1 | + | 3 - 2 | = 2.
- The closest cell of the path to the thief at cell (3, 0) is cell (3, 2). The distance between them is | 3 - 3 | + | 0 - 2 | = 2.
It can be shown that there are no other paths with a higher safeness factor.

Constraints:

    1 <= grid.length == n <= 400
    grid[i].length == n
    grid[i][j] is either 0 or 1.
    There is at least one thief in the grid.

---

This is a multi source BFS problem, IMO. We can perform a multi source
bfs from the thiefs into the rest of the grid, and record where they meet.

The intersection of the msbfs is the safest path. We just need to look for the
maximum value in that path.

That being said, if there's only 1 theif, then we're looking for the max distance,
recorded in the whole of res.

"""


class Solution:
    def maximumSafenessFactor(self, G: List[List[int]]) -> int:
        if G and G[0] and G[0][0] == 1 or G[-1][-1] == 1:
            return 0

        res = like(G)
        for i, j in cells(res):
            res[i][j] = -1

        q = deque([])

        for i, j in cells(G):
            if G[i][j] == 1:
                q.append([i, j, 0])

        safest_path = []

        while q:
            i, j, dist = q.popleft()
            if res[i][j] != -1:
                continue
            res[i][j] = dist
            nb = [*nbrs(G, i, j)]
            if nb:
                count = 0
                for ni, nj in nb:
                    if res[ni][nj] == -1:
                        count += 1
                        q.append([ni, nj, dist + 1])
                if count == 0:
                    print(ni, nj, dist)
                    safest_path.append(dist)

        print(res)

        return min(safest_path) if safest_path else 0


sol = Solution()

# print(sol.maximumSafenessFactor([[0, 0, 1], [0, 0, 0], [0, 0, 0]]))
# print(sol.maximumSafenessFactor([[1, 0, 0], [0, 0, 0], [0, 0, 1]]))  # 0

# assert sol.maximumSafenessFactor([[1, 0, 0], [0, 0, 0], [0, 0, 1]]) == 0
# sol.maximumSafenessFactor([[0, 0, 1], [0, 0, 0], [0, 0, 0]]) == 2
print(
    sol.maximumSafenessFactor([[0, 0, 0, 1], [0, 0, 0, 0], [0, 0, 0, 0], [1, 0, 0, 0]])
)

# assert sol.maximumSafenessFactor([[1]]) == 0
# assert sol.maximumSafenessFactor([[0, 1], [1, 0]]) == 0
# assert sol.maximumSafenessFactor([[0, 0, 0], [0, 1, 0], [0, 0, 0]]) == 1
# assert (
#     sol.maximumSafenessFactor([[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1]])
#     == 0
# )
# assert sol.maximumSafenessFactor([[1] * 5 for _ in range(5)]) == 0
# assert sol.maximumSafenessFactor([[0] * 5 for _ in range(5)]) == 0
# assert (
#     sol.maximumSafenessFactor(
#         [
#             [0, 0, 0, 0, 1],
#             [0, 1, 0, 0, 0],
#             [0, 0, 0, 1, 0],
#             [1, 0, 0, 0, 0],
#             [0, 0, 1, 0, 0],
#         ]
#     )
#     == 1
# )
# assert sol.maximumSafenessFactor([[0] * 400 for _ in range(400)]) == 0
# assert (
#     sol.maximumSafenessFactor([[1] + [0] * 399] + [[0] * 400 for _ in range(399)]) == 0
# )
# assert (
#     sol.maximumSafenessFactor([[0] * 399 + [1]] + [[0] * 400 for _ in range(399)])
#     == 399
# )
# assert (
#     sol.maximumSafenessFactor(
#         [[1 if (i + j) % 2 == 0 else 0 for j in range(10)] for i in range(10)]
#     )
#     == 0
# )


# FAILED: walked away after 25m 15s; no working solution.
# Judge the moves actually attempted as struggled, not clean.
