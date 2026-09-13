"""
URL: https://leetcode.com/problems/multi-source-flood-fill/description/?envType=problem-list-v2&envId=vn57k9wr

3905. Multi Source Flood Fill

You are given two integers n and m representing the number of rows and columns of a grid, respectively.

You are also given a 2D integer array sources, where sources[i] = [r_i, c_i, color_i] indicates that the cell (r_i, c_i) is initially colored with color_i. All other cells are initially uncolored and represented as 0.

At each time step, every currently colored cell spreads its color to all adjacent uncolored cells in the four directions: up, down, left, and right. All spreads happen simultaneously.

If multiple colors reach the same uncolored cell at the same time step, the cell takes the color with the maximum value.

The process continues until no more cells can be colored.

Return a 2D integer array representing the final state of the grid, where each cell contains its final color.

Example 1:

Input: n = 3, m = 3, sources = [[0,0,1],[2,2,2]]
Output: [[1,1,2],[1,2,2],[2,2,2]]
Explanation:
The grid at each time step is as follows:
At time step 2, cells (0, 2), (1, 1), and (2, 0) are reached by both colors, so they are assigned color 2 as it has the maximum value among them.

Example 2:

Input: n = 3, m = 3, sources = [[0,1,3],[1,1,5]]
Output: [[3,3,3],[5,5,5],[5,5,5]]
Explanation:
The grid at each time step is as follows:

Example 3:

Input: n = 2, m = 2, sources = [[1,1,5]]
Output: [[5,5],[5,5]]
Explanation:
The grid at each time step is as follows:
Since there is only one source, all cells are assigned the same color.

Constraints:

    1 <= n, m <= 10^5
    1 <= n * m <= 10^5
    1 <= sources.length <= n * m
    sources[i] = [r_i, c_i, color_i]
    0 <= r_i <= n - 1
    0 <= c_i <= m - 1
    1 <= color_i <= 10^6
    All (r_i, c_i) in sources are distinct.

---

'If multiple colors reach the same uncolored cell at the same time step, the cell takes the color with the maximum value.'

This is a tricky requirement. I'm thinking that the res matrix needs to track at which step the flood fill arrived,
and only take the max of the colour if the time is the same. So res needs to store an matrix of dicts or a 3d matrix

Not all asserts pass.

"""


class Solution:
    def colorGrid(self, n: int, m: int, sources: list[list[int]]) -> list[list[int]]:
        def bfs(i, j):
            pass

        res = []

        for i in range(n):
            res.append([[0, 0]] * m)

        orig = set([])
        for i, j, c in sources:
            res[i][j] = [c, 0]
            orig.add((i, j))

        q = deque([])
        for i, j, c in sources:
            q.append([i, j, c, 0])

        while q:
            i, j, c, time = q.popleft()

            if res[i][j][0] == 0 or res[i][j][1] == time:
                res[i][j] = [max(res[i][j][0], c), time]
            elif (i, j) not in orig:
                continue

            if i > 0:
                q.append([i - 1, j, c, time + 1])
            if i < len(res) - 1:
                q.append([i + 1, j, c, time + 1])
            if j > 0:
                q.append([i, j - 1, c, time + 1])
            if j < len(res[0]) - 1:
                q.append([i, j + 1, c, time + 1])

        for i in range(n):
            for j in range(m):
                res[i][j] = res[i][j][0]

        return res


sol = Solution()

print(sol.colorGrid(3, 3, [[0, 0, 1], [2, 2, 2]]))  # [[1,1,2],[1,2,2],[2,2,2]]

assert sol.colorGrid(3, 3, [[0, 0, 1], [2, 2, 2]]) == [[1, 1, 2], [1, 2, 2], [2, 2, 2]]
assert sol.colorGrid(3, 3, [[0, 1, 3], [1, 1, 5]]) == [[3, 3, 3], [5, 5, 5], [5, 5, 5]]
# assert sol.colorGrid(2, 2, [[1, 1, 5]]) == [[5, 5], [5, 5]]

# assert sol.colorGrid(1, 1, [[0, 0, 1]]) == [[1]]
# assert sol.colorGrid(2, 2, [[0, 0, 1], [1, 1, 1]]) == [[1, 1], [1, 1]]
# assert sol.colorGrid(3, 3, [[0, 0, 1], [0, 2, 2], [2, 0, 3], [2, 2, 4]]) == [
#     [1, 2, 2],
#     [3, 4, 4],
#     [3, 4, 4],
# ]
# assert sol.colorGrid(3, 3, [[1, 1, 5], [1, 2, 3]]) == [[5, 5, 3], [5, 5, 3], [5, 5, 3]]
# assert sol.colorGrid(4, 4, [[0, 0, 1], [0, 3, 2], [3, 0, 3], [3, 3, 4]]) == [
#     [1, 1, 2, 2],
#     [1, 1, 2, 2],
#     [3, 3, 4, 4],
#     [3, 3, 4, 4],
# ]
# assert sol.colorGrid(5, 5, [[2, 2, 10]]) == [
#     [10, 10, 10, 10, 10],
#     [10, 10, 10, 10, 10],
#     [10, 10, 10, 10, 10],
#     [10, 10, 10, 10, 10],
#     [10, 10, 10, 10, 10],
# ]
# assert sol.colorGrid(5, 5, [[0, 0, 1], [0, 4, 2], [4, 0, 3], [4, 4, 4], [2, 2, 5]]) == [
#     [1, 1, 5, 2, 2],
#     [1, 5, 5, 5, 2],
#     [5, 5, 5, 5, 5],
#     [3, 5, 5, 5, 4],
#     [3, 3, 5, 4, 4],
# ]
# assert sol.colorGrid(1, 10, [[0, 0, 1]]) == [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
# assert sol.colorGrid(10, 1, [[0, 0, 1]]) == [
#     [1],
#     [1],
#     [1],
#     [1],
#     [1],
#     [1],
#     [1],
#     [1],
#     [1],
#     [1],
# ]
# assert sol.colorGrid(
#     10, 10, [[0, 0, 1], [0, 9, 2], [9, 0, 3], [9, 9, 4], [5, 5, 1000000]]
# ) == [
#     [1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
#     [1, 1, 1, 1, 1000000, 1000000, 2, 2, 2, 2],
#     [1, 1, 1, 1000000, 1000000, 1000000, 1000000, 2, 2, 2],
#     [1, 1, 1000000, 1000000, 1000000, 1000000, 1000000, 1000000, 2, 2],
#     [1, 1000000, 1000000, 1000000, 1000000, 1000000, 1000000, 1000000, 1000000, 2],
#     [
#         3,
#         1000000,
#         1000000,
#         1000000,
#         1000000,
#         1000000,
#         1000000,
#         1000000,
#         1000000,
#         1000000,
#     ],
#     [3, 3, 1000000, 1000000, 1000000, 1000000, 1000000, 1000000, 1000000, 4],
#     [3, 3, 3, 1000000, 1000000, 1000000, 1000000, 1000000, 4, 4],
#     [3, 3, 3, 3, 1000000, 1000000, 1000000, 4, 4, 4],
#     [3, 3, 3, 3, 3, 1000000, 4, 4, 4, 4],
# ]
# assert sol.colorGrid(10, 10, [[i, i, i + 1] for i in range(10)]) == [
#     [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
#     [2, 2, 3, 4, 5, 6, 7, 8, 9, 10],
#     [3, 3, 3, 4, 5, 6, 7, 8, 9, 10],
#     [4, 4, 4, 4, 5, 6, 7, 8, 9, 10],
#     [5, 5, 5, 5, 5, 6, 7, 8, 9, 10],
#     [6, 6, 6, 6, 6, 6, 7, 8, 9, 10],
#     [7, 7, 7, 7, 7, 7, 7, 8, 9, 10],
#     [8, 8, 8, 8, 8, 8, 8, 8, 9, 10],
#     [9, 9, 9, 9, 9, 9, 9, 9, 9, 10],
#     [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
# ]
