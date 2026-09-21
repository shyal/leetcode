"""
URL: https://leetcode.com/problems/shortest-bridge/description/?envType=problem-list-v2&envId=vn57k9wr

934. Shortest Bridge

You are given an n x n binary matrix grid where 1 represents land and 0 represents water.

An island is a 4-directionally connected group of 1's not connected to any other 1's. There are exactly two islands in grid.

You may change 0's to 1's to connect the two islands to form one island.

Return the smallest number of 0's you must flip to connect the two islands.

Example 1:

Input: grid = [[0,1],[1,0]]
Output: 1

Example 2:

Input: grid = [[0,1,0],[0,0,0],[0,0,1]]
Output: 2

Example 3:

Input: grid = [[1,1,1,1,1],[1,0,0,0,1],[1,0,1,0,1],[1,0,0,0,1],[1,1,1,1,1]]
Output: 1

Constraints:

    n == grid.length == grid[i].length
    2 <= n <= 100
    grid[i][j] is either 0 or 1.
    There are exactly two islands in grid.


---

I'm wondering whether this is possible without tagging the islands.

"""


class Solution:
    def shortestBridge(self, grid: List[List[int]]) -> int:

        tags = like(grid, -1)

        def tag(i, j, t):
            if tags[i][j] != -1:
                return
            tags[i][j] = t
            for ni, nj in nbrs(grid, i, j):
                if grid[ni][nj] == 1:
                    tag(ni, nj, t)

        for i, j in cells(grid):
            if grid[i][j] == 1:
                tag(i, j, i * len(grid) + j)

        res = like(grid, inf)
        q = deque()
        seen = set()
        for i, j in cells(grid):
            if grid[i][j] == 1:
                q.append([i, j, 0, tags[i][j]])

        while q:
            i, j, dist, tag = q.popleft()
            if (i, j) in seen:
                continue
            seen.add((i, j, tag))
            if grid[i][j] == 1 and tags[i][j] != tag:
                print(dist)
            res[i][j] = dist
            for ni, nj in nbrs(grid, i, j):
                if grid[ni][nj] == 0 and (ni, nj, tag) not in seen:
                    q.append([ni, nj, dist + 1, tag])

        tabulate(res)

        return min(res[i][j] for i, j in cells(res))


sol = Solution()

sol.shortestBridge(
    [
        [1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 1, 1],
    ]
)

# print(sol.shortestBridge([[0, 1], [1, 0]]))  # 1

# assert sol.shortestBridge([[0, 1], [1, 0]]) == 1
# assert sol.shortestBridge([[0, 1, 0], [0, 0, 0], [0, 0, 1]]) == 2
# assert (
#     sol.shortestBridge(
#         [
#             [1, 1, 1, 1, 1],
#             [1, 0, 0, 0, 1],
#             [1, 0, 1, 0, 1],
#             [1, 0, 0, 0, 1],
#             [1, 1, 1, 1, 1],
#         ]
#     )
#     == 1
# )

# assert sol.shortestBridge([[1, 0], [0, 1]]) == 1
# assert sol.shortestBridge([[1, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 1]]) == 3
# assert (
#     sol.shortestBridge(
#         [
#             [1, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 1],
#             [0, 0, 0, 1, 1],
#         ]
#     )
#     == 6
# )
# assert sol.shortestBridge([[1] + [0] * 99] + [[0] * 100] * 98 + [[0] * 99 + [1]]) == -1
# assert sol.shortestBridge([[1, 0, 1]]) == -1
# assert (
#     sol.shortestBridge(
#         [
#             [0, 0, 0, 0, 1],
#             [0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0],
#             [1, 0, 0, 0, 0],
#         ]
#     )
#     == 7
# )
# assert (
#     sol.shortestBridge(
#         [
#             [1, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0],
#             [0, 0, 1, 0, 0],
#             [0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 1],
#         ]
#     )
#     == 3
# )
# assert (
#     sol.shortestBridge(
#         [
#             [1, 1, 1, 1, 1],
#             [1, 0, 0, 0, 1],
#             [1, 0, 0, 0, 1],
#             [1, 0, 0, 0, 1],
#             [1, 1, 1, 1, 1],
#         ]
#     )
#     == -1
# )
# assert (
#     sol.shortestBridge(
#         [
#             [1, 0, 0, 0, 1],
#             [0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0],
#             [1, 0, 0, 0, 1],
#         ]
#     )
#     == 3
# )
# assert sol.shortestBridge([[1, 0], [0, 1]]) == 1


# FAILED: walked away after 29m 24s; no working solution.
# Judge the moves actually attempted as struggled, not clean.
