"""
EPI 15.10 Implement a Sudoku solver

Given a 9 x 9 grid partial_assignment of integers 0 to 9, where 0 is a
blank cell, fill every blank in place so that every row, every column
and every 3 x 3 box holds each of 1 to 9 exactly once. The given digits
must not change. Return True when such a filling exists, and False when
none exists. When there are several fillings, any of them is accepted.

Example 1:

Input: partial_assignment = [[0, 0, 0, 7, 0, 0, 3, 0, 1],
                             [3, 0, 0, 9, 0, 0, 0, 0, 0],
                             [0, 4, 0, 3, 1, 0, 2, 0, 0],
                             [0, 6, 0, 4, 0, 0, 5, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 1, 0, 0, 8, 0, 4, 0],
                             [0, 0, 6, 0, 2, 1, 0, 5, 0],
                             [0, 0, 0, 0, 0, 9, 0, 0, 8],
                             [8, 0, 5, 0, 0, 4, 0, 0, 0]]
Output: True, and partial_assignment holds a full grid that keeps the
given digits.

Example 2:

Input: partial_assignment = [[0, 2, 3, 4, 5, 6, 7, 8, 9],
                             [1, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0]]
Output: False
Explanation: the given digits break no rule. Row 0 needs a 1 in its
blank, and column 0 already holds a 1.

Constraints:

    partial_assignment has 9 rows of 9 integers, each 0 to 9.
    The given digits break no rule.

    REQUIRED: NO copy of the grid per step. NO new grid: the filling
    goes into partial_assignment.
"""


class Solution:
    def solve_sudoku(self, partial_assignment: list[list[int]]) -> bool:
        pass


sol = Solution()


def grid(lines):
    return [[0 if c == "." else int(c) for c in line.split()] for line in lines]


def solved(board, start):
    """True when board is a full Sudoku grid that keeps the digits of start."""
    units = [board[i] for i in range(9)]
    units += [[board[i][j] for i in range(9)] for j in range(9)]
    units += [[board[r + i][c + j] for i in range(3) for j in range(3)] for r in (0, 3, 6) for c in (0, 3, 6)]
    keeps = all(start[i][j] in (0, board[i][j]) for i in range(9) for j in range(9))
    return keeps and all(sorted(u) == list(range(1, 10)) for u in units)


board = grid([
    ". . . 7 . . 3 . 1",
    "3 . . 9 . . . . .",
    ". 4 . 3 1 . 2 . .",
    ". 6 . 4 . . 5 . .",
    ". . . . . . . . .",
    ". . 1 . . 8 . 4 .",
    ". . 6 . 2 1 . 5 .",
    ". . . . . 9 . . 8",
    "8 . 5 . . 4 . . .",
])
print(sol.solve_sudoku(board))  # True
print(board)

# b = grid([". . . 7 . . 3 . 1", "3 . . 9 . . . . .", ". 4 . 3 1 . 2 . .", ". 6 . 4 . . 5 . .", ". . . . . . . . .", ". . 1 . . 8 . 4 .", ". . 6 . 2 1 . 5 .", ". . . . . 9 . . 8", "8 . 5 . . 4 . . ."])
# start = [row[:] for row in b]
# assert sol.solve_sudoku(b) is True
# assert solved(b, start)
# b = grid([". 2 3 4 5 6 7 8 9", "1 . . . . . . . ."] + [". . . . . . . . ."] * 7)
# assert sol.solve_sudoku(b) is False
# b = grid([". . . . . . . . ."] * 9)
# start = [row[:] for row in b]
# assert sol.solve_sudoku(b) is True
# assert solved(b, start)
# b = grid([". . 5 . . 2 . . .", ". . 9 . 4 7 . 2 .", ". . 8 . 5 6 . . 1", ". . . . . 8 3 4 .", ". . . . . . . . 6", ". . . . 3 . 1 8 .", ". 2 . . . . . . .", ". 9 . . 8 . 6 7 .", "3 . 6 5 7 . . . ."])
# start = [row[:] for row in b]
# assert sol.solve_sudoku(b) is True
# assert solved(b, start)
# b = grid([". . 3 8 . . 4 . .", ". . . . 1 . . 7 .", ". 6 . . . 5 . . 9", ". . . 9 . . 6 . .", ". 2 . . . . . 1 .", ". . 4 . . 3 . . 2", ". . 2 . . . 8 . .", ". 1 . . . . . 5 .", "9 . . . . 7 . . 3"])
# start = [row[:] for row in b]
# assert sol.solve_sudoku(b) is True
# assert solved(b, start)
# b = grid([". 8 9 . 4 . 6 . 5", ". 7 . . . 8 . 4 1", "5 6 . 9 . . . . 8", ". . . 7 . 5 . 9 .", ". 9 . 4 . 1 . 5 .", ". 3 . 9 . 6 . 1 .", "8 . . . . . . . 7", ". 2 . 8 . . . 6 .", ". . 6 . 7 . . 8 ."])
# assert sol.solve_sudoku(b) is False
# b = grid(["5 3 4 6 7 8 9 1 2", "6 7 2 1 9 5 3 4 8", "1 9 8 3 4 2 5 6 7", "8 5 9 7 6 1 4 2 3", "4 2 6 8 5 3 7 9 1", "7 1 3 9 2 4 8 5 6", "9 6 1 5 3 7 2 8 4", "2 8 7 4 1 9 6 3 5", "3 4 5 2 8 6 1 7 9"])
# start = [row[:] for row in b]
# assert sol.solve_sudoku(b) is True
# assert b == start
# b = grid([". 3 4 6 7 8 9 1 2", "6 7 2 1 9 5 3 4 8", "1 9 8 3 4 2 5 6 7", "8 5 9 7 6 1 4 2 3", "4 2 6 8 5 3 7 9 1", "7 1 3 9 2 4 8 5 6", "9 6 1 5 3 7 2 8 4", "2 8 7 4 1 9 6 3 5", "3 4 5 2 8 6 1 7 ."])
# assert sol.solve_sudoku(b) is True
# assert b[0][0] == 5 and b[8][8] == 9
