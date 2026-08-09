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

---



[
[2,1,1],
[1,1,0],
[0,1,1]
]

"""
from collections import namedtuple
class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        Cell = namedtuple('Cell', ['row', 'col'])
        def get_neighbours(row, col):
            N = []
            if row > 0 and grid[row-1][col] == 1:
                N.append(Cell(row-1, col))
            if row < len(grid)-1 and grid[row+1][col] == 1:
                N.append(Cell(row+1, col))
            if col > 0 and grid[row][col -1] == 1:
                N.append(Cell(row, col-1))
            if col < len(grid[0]) -1 and grid[row][col + 1] == 1:
                N.append(Cell(row, col+1))
            return N

        queue = deque()
        has_fresh_oranges = False
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 2:
                    queue.append(Cell(i, j))
                elif grid[i][j] == 1:
                    has_fresh_oranges = True

        if not has_fresh_oranges:
            return 0

        if not queue:
            return -1

        time = 0
        while queue:
            time += 1
            neighbours = set([])
            for cell in queue:
                N = get_neighbours(cell.row, cell.col)
                for n in N:
                    neighbours.add(n)
                    grid[n.row][n.col] = 2
            queue = deque(neighbours)

        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 1:
                    return -1

        return time -1


sol = Solution()

print(sol.orangesRotting([[2, 1, 1], [1, 1, 0], [0, 1, 1]]))  # 4

assert sol.orangesRotting([[2, 1, 1], [1, 1, 0], [0, 1, 1]]) == 4
assert sol.orangesRotting([[2, 1, 1], [0, 1, 1], [1, 0, 1]]) == -1
assert sol.orangesRotting([[0, 2]]) == 0
assert sol.orangesRotting([[0]]) == 0
assert sol.orangesRotting([[1]]) == -1
assert sol.orangesRotting([[2]]) == 0
assert sol.orangesRotting([[1, 2]]) == 1
assert sol.orangesRotting([[2, 0, 1]]) == -1
assert sol.orangesRotting([[0, 0], [0, 0]]) == 0
assert sol.orangesRotting([[2, 0], [0, 2]]) == 0
assert sol.orangesRotting([[2, 2], [1, 1]]) == 1
assert sol.orangesRotting([[2, 1, 1, 1, 1]]) == 4
assert sol.orangesRotting([[1], [1], [2], [1]]) == 2
assert sol.orangesRotting([[2, 1, 1], [1, 1, 1], [1, 1, 1]]) == 4
assert sol.orangesRotting([[2, 1, 1], [1, 1, 1], [1, 1, 2]]) == 2
assert sol.orangesRotting([[1, 0, 2], [0, 0, 0], [2, 0, 1]]) == -1
assert sol.orangesRotting([[2, 1, 0, 1]]) == -1
assert sol.orangesRotting([[1, 1, 1], [1, 2, 1], [1, 1, 1]]) == 2
assert (
    sol.orangesRotting(
        [[2 if r == 0 and c == 0 else 1 for c in range(10)] for r in range(10)]
    )
    == 18
)