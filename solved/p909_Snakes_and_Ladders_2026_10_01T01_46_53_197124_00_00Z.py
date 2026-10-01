"""
URL: https://leetcode.com/problems/snakes-and-ladders/description/?envType=problem-list-v2&envId=vn57k9wr

909. Snakes and Ladders

You are given an n x n integer matrix board where the cells are labeled from 1 to n^2 in a Boustrophedon style starting from the bottom left of the board (i.e. board[n - 1][0]) and alternating direction each row.

You start on square 1 of the board. In each move, starting from square curr, do the following:

- Choose a destination square next with a label in the range [curr + 1, min(curr + 6, n^2)].
  - This choice simulates the result of a standard 6-sided die roll: i.e., there are always at most 6 destinations, regardless of the size of the board.
- If next has a snake or ladder, you must move to the destination of that snake or ladder. Otherwise, you move to next.
- The game ends when you reach the square n^2.

A board square on row r and column c has a snake or ladder if board[r][c] != -1. The destination of that snake or ladder is board[r][c]. Squares 1 and n^2 are not the starting points of any snake or ladder.

Note that you only take a snake or ladder at most once per dice roll. If the destination to a snake or ladder is the start of another snake or ladder, you do not follow the subsequent snake or ladder.

For example, suppose the board is [[-1,4],[-1,3]], and on the first move, your destination square is 2. You follow the ladder to square 3, but do not follow the subsequent ladder to 4.

Return the least number of dice rolls required to reach the square n^2. If it is not possible to reach the square, return -1.

Example 1:

Input: board = [[-1,-1,-1,-1,-1,-1],
                [-1,-1,-1,-1,-1,-1],
                [-1,-1,-1,-1,-1,-1],
                [-1,35,-1,-1,13,-1],
                [-1,-1,-1,-1,-1,-1],
                [-1,15,-1,-1,-1,-1]]
Output: 4
Explanation:
In the beginning, you start at square 1 (at row 5, column 0).
You decide to move to square 2 and must take the ladder to square 15.
You then decide to move to square 17 and must take the snake to square 13.
You then decide to move to square 14 and must take the ladder to square 35.
You then decide to move to square 36, ending the game.
This is the lowest possible number of moves to reach the last square, so return 4.

Example 2:

Input: board = [[-1,-1],[-1,3]]
Output: 1

Constraints:

    n == board.length == board[i].length
    2 <= n <= 20
    board[i][j] is either -1 or in the range [1, n^2].
    The squares labeled 1 and n^2 are not the starting points of any snake or ladder.
---
Got hinted: made a mistke with parity test
The parity test in posToGrid is on n - 1 - pos // n, the row from the top. On a 5 by 5 board the bottom row is r = 4, which is even, so it gets mirrored when it should run left to right, and every row after it is wrong too. Square 25 lands on [0, 0], where the board holds 2, so the last square always sends you back to 2 and the search returns -1.

LEETCODE: Accepted (47 ms, 19.5 MB)
"""


# mu 0.7
# def posToGrid(pos, n)
#   pos -= 1
#   [n - 1 - (pos) // n, pos % n if (pos // n) % 2 == 0 else (n - 1 - pos % n)]
#
# def gridToPos(r, c, n)
#   (n - 1 - r) * n + (c if r % 2 else (n - 1 - c)) + 1
#
# def snakesAndLadders(board: [[int]]) -> int
#   n = len(board)
#   q = deque([[0, 1, False]])
#   seen = set()
#   while q
#     throws, curr, skip = q.popleft()
#     if (curr) in seen
#       continue
#     seen.add((curr))
#     if curr >= n * n
#       return throws
#     for newpos in reversed(range(curr + 1, min(curr + 6, n**2) + 1))
#       r, c = self.posToGrid(newpos, n)
#       if board[r][c] == -1
#         q.append([throws + 1, newpos, False])
#       else
#         q.append([throws + 1, board[r][c], True])
#   -1

class Grid(list):
    """A list of rows that also takes a (row, col) pair as an index."""

    def __getitem__(self, k):
        if type(k) is tuple:
            return list.__getitem__(self, k[0])[k[1]]
        return list.__getitem__(self, k)

    def __setitem__(self, k, v):
        if type(k) is tuple:
            list.__getitem__(self, k[0])[k[1]] = v
        else:
            list.__setitem__(self, k, v)


class Solution:
    def posToGrid(self, pos, n):
        pos -= 1
        return [n - 1 - (pos) // n, pos % n if (pos // n) % 2 == 0 else (n - 1 - pos % n)]

    def gridToPos(self, r, c, n):
        return (n - 1 - r) * n + (c if r % 2 else (n - 1 - c)) + 1

    def snakesAndLadders(self, board: list[list[int]]) -> int:
        _in_board, board = board, Grid(board)
        _w_board = board
        try:
            n = len(board)
            q = deque([[0, 1, False]])
            seen = set()
            while q:
                throws, curr, skip = q.popleft()
                if (curr) in seen:
                    continue
                seen.add((curr))
                if curr >= n * n:
                    return throws
                for newpos in reversed(range(curr + 1, min(curr + 6, n ** 2) + 1)):
                    r, c = self.posToGrid(newpos, n)
                    if board[r][c] == -1:
                        q.append([throws + 1, newpos, False])
                    else:
                        q.append([throws + 1, board[r][c], True])
            return -1
        finally:
            _in_board[:] = _w_board


sol = Solution()
assert sol.snakesAndLadders([[2, -1, -1, -1, -1], [-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1]]) == 4
assert sol.snakesAndLadders([[-1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1], [-1, 35, -1, -1, 13, -1], [-1, -1, -1, -1, -1, -1], [-1, 15, -1, -1, -1, -1]]) == 4
assert sol.snakesAndLadders([[-1, -1], [-1, 3]]) == 1
assert Solution().snakesAndLadders([[-1, -1], [-1, -1]]) == 1
assert Solution().snakesAndLadders([[-1, 2], [-1, -1]]) == 1
assert Solution().snakesAndLadders([[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]) == 2
assert Solution().snakesAndLadders([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]) == 1
assert Solution().snakesAndLadders([[-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1]]) == 3
assert Solution().snakesAndLadders([[-1 for _ in range(0, 20)] for _ in range(0, 20)]) == 67
assert Solution().snakesAndLadders([[-1] * 19 + [400]] + [[-1] * 20 for _ in range(0, 19)]) == 64
assert Solution().snakesAndLadders([[-1] * 19 + [381]] + [[-1] * 20 for _ in range(0, 19)]) == 67
assert Solution().snakesAndLadders([[-1] * 20 for _ in range(0, 19)] + [[-1] * 19 + [399]]) == 5
assert Solution().snakesAndLadders([[-1] * 20 for _ in range(0, 19)] + [[-1] * 19 + [380]]) == 8
assert Solution().snakesAndLadders([[-1] * 20 for _ in range(0, 20)]) == 67
assert Solution().snakesAndLadders([[-1] * 20 for _ in range(0, 20)]) == 67
