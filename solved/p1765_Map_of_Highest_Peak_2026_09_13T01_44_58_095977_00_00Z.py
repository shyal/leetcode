"""
URL: https://leetcode.com/problems/map-of-highest-peak/description/?envType=problem-list-v2&envId=vn57k9wr

1765. Map of Highest Peak

You are given an integer matrix isWater of size m x n that represents a map of land and water cells.

- If isWater[i][j] == 0, cell (i, j) is a land cell.
- If isWater[i][j] == 1, cell (i, j) is a water cell.

You must assign each cell a height in a way that follows these rules:

- The height of each cell must be non-negative.
- If the cell is a water cell, its height must be 0.
- Any two adjacent cells must have an absolute height difference of at most 1. A cell is adjacent to another cell if the former is directly north, east, south, or west of the latter (i.e., their sides are touching).

Find an assignment of heights such that the maximum height in the matrix is maximized.

Return an integer matrix height of size m x n where height[i][j] is cell (i, j)'s height. If there are multiple solutions, return any of them.

Example 1:

Input: isWater = [[0,1],[0,0]]
Output: [[1,0],[2,1]]
Explanation: The image shows the assigned heights of each cell.
The blue cell is the water cell, and the green cells are the land cells.

Example 2:

Input: isWater = [[0,0,1],[1,0,0],[0,0,0]]
Output: [[1,1,0],[0,1,1],[1,2,2]]
Explanation: A height of 2 is the maximum possible height of any assignment.
Any height assignment that has a maximum height of 2 while still meeting the rules will also be accepted.

Constraints:

    m == isWater.length
    n == isWater[i].length
    1 <= m, n <= 1000
    isWater[i][j] is 0 or 1.
    There is at least one water cell.

Note: This question is the same as 542: https://leetcode.com/problems/01-matrix/description/

---

From what i can tell this is very similar to 1162 (my previous solve).

Let's say, a multi-bfs,

"""


class Solution:
    def highestPeak(self, isWater: List[List[int]]) -> List[List[int]]:
        def bfs(i, j):
            q = deque([[i, j, 0]])
            visited = set([])
            while q:
                ii, jj, dist = q.popleft()
                if (ii, jj) in visited:
                    continue
                visited.add((ii, jj))

                if isWater[ii][jj] != 1:
                    res[ii][jj] = min(res[ii][jj], dist)

                if ii > 0:
                    q.append([ii - 1, jj, dist + 1])
                if ii < len(isWater) - 1:
                    q.append([ii + 1, jj, dist + 1])
                if jj > 0:
                    q.append([ii, jj - 1, dist + 1])
                if jj < len(isWater[0]) - 1:
                    q.append([ii, jj + 1, dist + 1])

        res = []
        for i in range(len(isWater)):
            res.append([float("inf")] * len(isWater[0]))

        has_ones = False
        for i in range(len(isWater)):
            for j in range(len(isWater[0])):
                if isWater[i][j] == 1:
                    has_ones = True
                    bfs(i, j)

        for i in range(len(isWater)):
            for j in range(len(isWater[0])):
                if has_ones:
                    if res[i][j] == float("inf"):
                        res[i][j] = 0
                else:
                    res[i][j] = -1

        return res


sol = Solution()

print(sol.highestPeak([[0, 1], [0, 0]]))  # [[1,0],[2,1]]

assert sol.highestPeak([[0, 1], [0, 0]]) == [[1, 0], [2, 1]]
assert sol.highestPeak([[0, 0, 1], [1, 0, 0], [0, 0, 0]]) == [
    [1, 1, 0],
    [0, 1, 1],
    [1, 2, 2],
] or sol.highestPeak([[0, 0, 1], [1, 0, 0], [0, 0, 0]]) == [
    [1, 1, 0],
    [0, 1, 1],
    [1, 2, 2],
]  # Accept any valid solution with max height 2.

assert sol.highestPeak([[1]]) == [[0]]
assert sol.highestPeak([[0]]) == [[-1]]
assert sol.highestPeak([[1, 0, 0, 0, 1]]) == [[0, 1, 2, 1, 0]]
assert sol.highestPeak([[0, 0, 0, 0, 0]]) == [[-1, -1, -1, -1, -1]]
assert sol.highestPeak([[1], [0], [0], [0], [1]]) == [[0], [1], [2], [1], [0]]
assert sol.highestPeak([[0], [0], [0], [0], [0]]) == [[-1], [-1], [-1], [-1], [-1]]
assert sol.highestPeak([[1] * 10]) == [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
assert sol.highestPeak([[0] * 10]) == [[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]]
