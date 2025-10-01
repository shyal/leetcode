"""
URL: https://leetcode.com/problems/rotting-oranges/description/?envType=study-plan-v2&envId=leetcode-75

994. Rotting Oranges

You are given an m x n grid where each cell can have one of three values:

        0 representing an empty cell,
        1 representing a fresh orange, or
        2 representing a rotten orange.

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

"""
Notes:

One solution is to linearly search for all rotten oranges, load them onto a deque
and perform a BFS. Let's handle the case where we begin with multiple rotten oranges
because 



"""

from collections import deque
from typing import List
from itertools import chain


class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        D = deque()
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 2:
                    D.append((i, j, 0))

        time = 0
        while D:
            ri, rj, s = D.popleft()
            time = max(time, s)
            val = grid[ri][rj]
            if ri - 1 >= 0 and grid[ri - 1][rj] == 1:
                grid[ri - 1][rj] = 2
                D.append([ri - 1, rj, s + 1])
            if ri + 1 < len(grid) and grid[ri + 1][rj] == 1:
                grid[ri + 1][rj] = 2
                D.append([ri + 1, rj, s + 1])
            if rj - 1 >= 0 and grid[ri][rj - 1] == 1:
                grid[ri][rj - 1] = 2
                D.append([ri, rj - 1, s + 1])
            if rj + 1 < len(grid[0]) and grid[ri][rj + 1] == 1:
                grid[ri][rj + 1] = 2
                D.append([ri, rj + 1, s + 1])

        has_ones = any(x == 1 for x in chain(*grid))
        return -1 if has_ones else time


sol = Solution()

test_cases = [
    ([[2, 1, 1], [1, 1, 0], [0, 1, 1]], 4),
    ([[2, 1, 1], [0, 1, 1], [1, 0, 1]], -1),
    ([[0, 2]], 0),
    ([[0]], 0),
    ([[1]], -1),
    ([[2]], 0),
    ([[2, 1], [1, 0]], 1),
    ([[2, 1, 1, 1]], 3),
    ([[2, 1, 0], [0, 1, 2]], 1),
    ([[1, 0, 1], [0, 2, 0]], -1),
]

for i, (grid, expected) in enumerate(test_cases, 1):
    actual = sol.orangesRotting(grid)
    assert actual == expected
