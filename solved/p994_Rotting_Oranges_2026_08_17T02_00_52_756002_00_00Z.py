"""
URL: https://leetcode.com/problems/rotting-oranges/description/?envType=problem-list-v2&envId=vn57k9wr

994. Rotting Oranges

You are given an m x n grid where each cell can have one of three values:

    - 0 representing an empty cell,
    - 1 representing a fresh orange, or
    - 2 representing a rotten orange.

Every minute, any fresh orange that is 4-directionally adjacent to a rotten
orange becomes rotten.

Return the minimum number of minutes that must elapse until no cell has a
fresh orange. If this is impossible, return -1.


Example 1:

Input: grid = [[2,1,1],[1,1,0],[0,1,1]]
Output: 4

Example 2:

Input: grid = [[2,1,1],[0,1,1],[1,0,1]]
Output: -1
Explanation: The orange in the bottom left corner (row 2, column 0) is never
rotten, because rotting only happens 4-directionally.

Example 3:

Input: grid = [[0,2]]
Output: 0
Explanation: Since there are already no fresh oranges at minute 0, the answer
is just 0.


Constraints:

    m == grid.length
    n == grid[i].length
    1 <= m, n <= 10
    grid[i][j] is 0, 1, or 2.
"""


class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        _max = 0
        Q = deque([])
        queued = set([])
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 2:
                    Q.append(((i, j), 0))
                    queued.add((i, j))
        while Q:
            pos, time = Q.popleft()
            x, y = pos
            grid[x][y] = -1
            _max = max(_max, time)
            if x > 0 and grid[x-1][y] == 1  and (x-1, y) not in queued:
                queued.add((x-1, y))
                Q.append(((x -1, y), time + 1))
            if x < len(grid) -1 and grid[x+1][y] == 1  and (x+1, y) not in queued:
                queued.add((x+1, y))
                Q.append(((x +1, y), time + 1))
            if y > 0 and grid[x][y-1] == 1 and (x, y-1) not in queued:
                queued.add((x, y-1))
                Q.append(((x, y - 1), time + 1))
            if y < len(grid[0]) -1 and grid[x][y+1] == 1 and (x, y+1) not in queued:
                queued.add((x, y+1))
                Q.append(((x, y + 1), time + 1))
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 1:
                    return -1
        return _max

sol = Solution()

# print(sol.orangesRotting([[2, 1, 1], [1, 1, 0], [0, 1, 1]]))  # 4

assert sol.orangesRotting([[2, 2],[1, 1],[0, 0],[2, 0]]) == 1
assert sol.orangesRotting([[2, 1, 1], [1, 1, 0], [0, 1, 1]]) == 4
assert sol.orangesRotting([[2, 1, 1], [0, 1, 1], [1, 0, 1]]) == -1
assert sol.orangesRotting([[0, 2]]) == 0
assert sol.orangesRotting([[0]]) == 0
assert sol.orangesRotting([[2]]) == 0
assert sol.orangesRotting([[1]]) == -1
assert sol.orangesRotting([[1, 2]]) == 1
assert sol.orangesRotting([[2, 0, 1]]) == -1
assert sol.orangesRotting([[0, 0], [0, 0]]) == 0
assert sol.orangesRotting([[2, 2], [2, 2]]) == 0
assert sol.orangesRotting([[1, 1], [1, 1]]) == -1
assert sol.orangesRotting([[2, 1], [1, 1]]) == 2
assert sol.orangesRotting([[2, 1, 1, 1, 1]]) == 4
assert sol.orangesRotting([[2, 1, 1, 1, 2]]) == 2
assert sol.orangesRotting([[1], [1], [2], [1]]) == 2
assert sol.orangesRotting([[2, 1, 1], [1, 1, 1], [0, 1, 2]]) == 2
assert sol.orangesRotting([[2, 1, 1], [0, 0, 1], [1, 1, 1]]) == 6