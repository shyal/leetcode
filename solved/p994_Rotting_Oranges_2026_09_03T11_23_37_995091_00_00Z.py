"""
URL: https://leetcode.com/problems/rotting-oranges/description/?envType=problem-list-v2&envId=vn57k9wr

994. Rotting Oranges

You are given an m x n grid where each cell can have one of three values:

- 0 representing an empty cell,
- 1 representing a fresh orange, or
- 2 representing a rotten orange.

Every minute, any fresh orange that is 4-directionally adjacent to a rotten orange becomes rotten.

Return the minimum number of minutes that must elapse until no cell has a fresh orange. If this is impossible, return -1.

Example 1:

Input: grid = [[2,1,1],[1,1,0],[0,1,1]]
Output: 4

Example 2:

Input: grid = [[2,1,1],[0,1,1],[1,0,1]]
Output: -1
Explanation: The orange in the bottom left corner (row 2, column 0) is never rotten, because rotting only happens 4-directionally.

Example 3:

Input: grid = [[0,2]]
Output: 0
Explanation: Since there are already no fresh oranges at minute 0, the answer is just 0.

Constraints:

    m == grid.length
    n == grid[i].length
    1 <= m, n <= 10
    grid[i][j] is 0, 1, or 2.
"""


class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        def bfs():
            res = 0
            q = deque([])
            visited = set([])
            for i in range(len(grid)):
                for j in range(len(grid[0])):
                    if grid[i][j] == 2:
                        q.append((i, j, 0))

            if not q:
                return 0

            while q:
                row, col, dist = q.popleft()
                if (row, col) in visited or grid[row][col] == 0:
                    continue
                visited.add((row, col))
                grid[row][col] = 0
                res = max(res, dist)

                if row > 0:
                    q.append((row - 1, col, dist + 1))
                if row < len(grid) - 1:
                    q.append((row + 1, col, dist + 1))
                if col > 0:
                    q.append((row, col - 1, dist + 1))
                if col < len(grid[0]) - 1:
                    q.append((row, col + 1, dist + 1))

            return res

        res = bfs()

        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 1:
                    return -1

        return res


sol = Solution()

print(sol.orangesRotting([[2, 1, 1], [1, 1, 0], [0, 1, 1]]))  # 4

assert sol.orangesRotting([[2, 1, 1], [1, 1, 0], [0, 1, 1]]) == 4
assert sol.orangesRotting([[2, 1, 1], [0, 1, 1], [1, 0, 1]]) == -1
assert sol.orangesRotting([[0, 2]]) == 0

assert sol.orangesRotting([[1]]) == -1
assert sol.orangesRotting([[2]]) == 0
assert sol.orangesRotting([[0]]) == 0
assert sol.orangesRotting([[1, 1, 1, 1, 1]]) == -1
assert sol.orangesRotting([[2, 0, 0, 0, 1]]) == -1
assert (
    sol.orangesRotting(
        [
            [2, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
        ]
    )
    == 8
)
assert sol.orangesRotting([[2] + [1] * 9] + [[1] * 10 for _ in range(9)]) == 18
assert sol.orangesRotting([[0] * 10 for _ in range(10)]) == 0
assert sol.orangesRotting([[2] + [0] * 9] + [[0] * 10 for _ in range(9)]) == 0
assert sol.orangesRotting([[1, 2, 1], [2, 1, 2], [1, 2, 1]]) == 1
assert sol.orangesRotting([[1, 1, 1], [1, 2, 1], [1, 1, 1]]) == 2
assert (
    sol.orangesRotting([[2] + [1] * 9] + [[1] * 10 for _ in range(8)] + [[1] * 9 + [0]])
    == 17
)
