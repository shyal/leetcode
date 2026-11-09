"""
EPI 18.1 Search a maze

Given a 2D list maze of 0s and 1s, where 0 is an open cell and 1 is a
wall, and two open cells s and e as (row, col) tuples, return a path from
s to e. A path is a list of (row, col) tuples that starts at s, ends at e,
holds only open cells, and has each cell share a side with the cell after
it. Return [] when there is no path. Any path is correct.

Example 1:

Input: maze = [[0, 0, 1, 0, 0],
               [1, 0, 1, 0, 1],
               [0, 0, 0, 0, 0],
               [0, 1, 1, 1, 0]], s = (0, 0), e = (0, 4)
Output: [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2), (2, 3), (1, 3), (0, 3), (0, 4)]
Explanation: the walls at (0, 2) and (1, 2) block the top row, so the
path goes down to row 2 and back up through (1, 3).

Example 2:

Input: maze = [[0, 1, 0]], s = (0, 0), e = (0, 2)
Output: []

Example 3:

Input: maze = [[0]], s = (0, 0), e = (0, 0)
Output: [(0, 0)]

Constraints:

    1 <= len(maze) <= 100
    1 <= len(maze[0]) <= 100
    maze[i][j] is 0 or 1, and the cells s and e are 0.
    maze may be changed.

    REQUIRED: O(rows * cols) time. NO recursion.
"""


class Solution:
    def search_maze(self, maze: list[list[int]], s: tuple[int, int], e: tuple[int, int]) -> list[tuple[int, int]]:
        pass


sol = Solution()

print(sol.search_maze([[0, 0, 1, 0, 0], [1, 0, 1, 0, 1], [0, 0, 0, 0, 0], [0, 1, 1, 1, 0]], (0, 0), (0, 4)))  # [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2), (2, 3), (1, 3), (0, 3), (0, 4)]

# check = lambda maze, s, e: (p := sol.search_maze([row[:] for row in maze], s, e)) != [] and p[0] == s and p[-1] == e and all(maze[r][c] == 0 for r, c in p) and all(abs(r1 - r2) + abs(c1 - c2) == 1 for (r1, c1), (r2, c2) in pairwise(p))
# assert sol.search_maze([[0, 0, 1, 0, 0], [1, 0, 1, 0, 1], [0, 0, 0, 0, 0], [0, 1, 1, 1, 0]], (0, 0), (0, 4)) == [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2), (2, 3), (1, 3), (0, 3), (0, 4)]
# assert sol.search_maze([[0, 1, 0]], (0, 0), (0, 2)) == []
# assert sol.search_maze([[0]], (0, 0), (0, 0)) == [(0, 0)]
# assert check([[0, 0, 1, 0, 0], [1, 0, 1, 0, 1], [0, 0, 0, 0, 0], [0, 1, 1, 1, 0]], (0, 4), (0, 0))
# assert check([[0, 0, 1, 0, 0], [1, 0, 1, 0, 1], [0, 0, 0, 0, 0], [0, 1, 1, 1, 0]], (3, 0), (3, 4))
# assert check([[0, 0], [0, 0]], (0, 0), (1, 1))
# assert check([[0, 0, 0]], (0, 2), (0, 0))
# assert check([[0], [0], [0]], (0, 0), (2, 0))
# assert sol.search_maze([[0, 1], [1, 0]], (0, 0), (1, 1)) == []
# assert sol.search_maze([[0, 0, 0], [1, 1, 1], [0, 0, 0]], (0, 0), (2, 2)) == []
# assert check([[0] * 100 for _ in range(100)], (0, 0), (99, 99))
# assert check([[0] * 100 for _ in range(100)], (99, 99), (0, 0))
# snake = [[0] * 100 if i % 2 == 0 else [1] * 99 + [0] if i % 4 == 1 else [0] + [1] * 99 for i in range(99)]
# assert check(snake, (0, 0), (98, 99))
# assert check(snake, (98, 99), (0, 0))
# assert sol.search_maze([[1] * 100 if i == 50 else [0] * 100 for i in range(100)], (0, 0), (99, 99)) == []
