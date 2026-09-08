"""
URL: https://leetcode.com/problems/maximum-number-of-moves-in-a-grid/description/?envType=problem-list-v2&envId=vn57k9wr

2684. Maximum Number of Moves in a Grid

You are given a 0-indexed m x n matrix grid consisting of positive integers.

You can start at any cell in the first column of the matrix, and traverse the grid in the following way:

- From a cell (row, col), you can move to any of the cells: (row - 1, col + 1), (row, col + 1) and (row + 1, col + 1) such that the value of the cell you move to, should be strictly bigger than the value of the current cell.

Return the maximum number of moves that you can perform.

Example 1:

Input: grid = [[2,4,3,5],[5,4,9,3],[3,4,2,11],[10,9,13,15]]
Output: 3
Explanation: We can start at the cell (0, 0) and make the following moves:
- (0, 0) -> (0, 1).
- (0, 1) -> (1, 2).
- (1, 2) -> (2, 3).
It can be shown that it is the maximum number of moves that can be made.

Example 2:

Input: grid = [[3,2,4],[2,1,9],[1,1,7]]
Output: 0
Explanation: Starting from any cell in the first column we cannot perform any moves.

Constraints:

    m == grid.length
    n == grid[i].length
    2 <= m, n <= 1000
    4 <= m * n <= 10^5
    1 <= grid[i][j] <= 10^6
"""


class Solution:
    def maxMoves(self, grid: List[List[int]]) -> int:
        @cache
        def dfs(i, j):
            if j == len(grid[0]) - 1:
                return 1
            ne, e, se = False, False, False
            if i - 1 > 0 and j + 1 < len(grid[0]):
                if grid[i - 1, j + 1] > grid[i][j]:
                    ne = dfs(i - 1, j + 1)
            if j < len(grid[0]):
                if grid[i][j + 1] > grid[i][j]:
                    e = dfs(i, j + 1)
            if i < len(grid) + 1 and j + 1 < len(grid[0]):
                if grid[i + 1][j + 1] > grid[i][j]:
                    se = dfs(i + 1, j + 1)
            if any([ne, e, se]):
                return max([ne, e, se]) + 1
            return 0

        return dfs(0, 0)


sol = Solution()

print(sol.maxMoves([[2, 4, 3, 5], [5, 4, 9, 3], [3, 4, 2, 11], [10, 9, 13, 15]]))  # 3

# assert sol.maxMoves([[2, 4, 3, 5], [5, 4, 9, 3], [3, 4, 2, 11], [10, 9, 13, 15]]) == 3
assert sol.maxMoves([[3, 2, 4], [2, 1, 9], [1, 1, 7]]) == 0

assert sol.maxMoves([[1, 2]]) == 1
# assert sol.maxMoves([[1], [2]]) == 0
# assert sol.maxMoves([[1, 1, 1, 1]]) == 0
# assert sol.maxMoves([[1], [1], [1], [1]]) == 0
# assert sol.maxMoves([[1, 2, 3, 4, 5]]) == 4
# assert sol.maxMoves([[5, 4, 3, 2, 1]]) == 0
# assert sol.maxMoves([[1, 2], [2, 3], [3, 4], [4, 5]]) == 1
# assert sol.maxMoves([[5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5]]) == 0
# assert sol.maxMoves([[1] * 1000 for _ in range(100)]) == 0
# assert sol.maxMoves([[i for i in range(1000)] for _ in range(100)]) == 999
# assert sol.maxMoves([[10**6 - j for j in range(1000)] for _ in range(100)]) == 0
# assert sol.maxMoves([[1, 1000000] * 500]) == 1


# FAILED: walked away after 26m 52s; no working solution.
# Judge the moves actually attempted as struggled, not clean.
