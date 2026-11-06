"""
Given a 9 x 9 board of the characters '1' to '9' and '.', where '.' is
a blank cell, return True when the blanks can be filled so that every
row, every column and every 3 x 3 box holds each of '1' to '9' exactly
once. Return False when no such filling exists.

Example 1:

Input: board = [". 2 3 4 5 6 7 8 9",
                "1 . . . . . . . .",
                ". . . . . . . . .",
                ". . . . . . . . .",
                ". . . . . . . . .",
                ". . . . . . . . .",
                ". . . . . . . . .",
                ". . . . . . . . .",
                ". . . . . . . . ."]
Output: False
Explanation: the given digits break no rule. Row 0 forces its blank to
be '1', and column 0 already holds a '1'.

Example 2:

Input: board = [". . . 7 . . 3 . 1",
                "3 . . 9 . . . . .",
                ". 4 . 3 1 . 2 . .",
                ". 6 . 4 . . 5 . .",
                ". . . . . . . . .",
                ". . 1 . . 8 . 4 .",
                ". . 6 . 2 1 . 5 .",
                ". . . . . 9 . . 8",
                "8 . 5 . . 4 . . ."]
Output: True

Example 3:

Input: board = the 9 x 9 board of only '.'
Output: True

Constraints:

    board has 9 rows of 9 characters, each '1' to '9' or '.'.
    The board is given as a list of lists of one-character strings.

    REQUIRED: O(1) time to test whether a digit may go in a cell. NO
    scan of a row, a column or a box per test. NO copy of the board per
    step.
"""


class Solution:
    def sudoku_solve(self, board: list[list[str]]) -> bool:
        pass


sol = Solution()


def rows(*lines):
    return [line.split() for line in lines]


print(
    sol.sudoku_solve(
        rows(
            ". 2 3 4 5 6 7 8 9",
            "1 . . . . . . . .",
            ". . . . . . . . .",
            ". . . . . . . . .",
            ". . . . . . . . .",
            ". . . . . . . . .",
            ". . . . . . . . .",
            ". . . . . . . . .",
            ". . . . . . . . .",
        )
    )
)  # False

# assert sol.sudoku_solve(rows(". 2 3 4 5 6 7 8 9", "1 . . . . . . . .", ". . . . . . . . .", ". . . . . . . . .", ". . . . . . . . .", ". . . . . . . . .", ". . . . . . . . .", ". . . . . . . . .", ". . . . . . . . .")) is False
# assert sol.sudoku_solve(rows(". . . 7 . . 3 . 1", "3 . . 9 . . . . .", ". 4 . 3 1 . 2 . .", ". 6 . 4 . . 5 . .", ". . . . . . . . .", ". . 1 . . 8 . 4 .", ". . 6 . 2 1 . 5 .", ". . . . . 9 . . 8", "8 . 5 . . 4 . . .")) is True
# assert sol.sudoku_solve(rows(*[". . . . . . . . ."] * 9)) is True
# assert sol.sudoku_solve(rows(". 8 9 . 4 . 6 . 5", ". 7 . . . 8 . 4 1", "5 6 . 9 . . . . 8", ". . . 7 . 5 . 9 .", ". 9 . 4 . 1 . 5 .", ". 3 . 9 . 6 . 1 .", "8 . . . . . . . 7", ". 2 . 8 . . . 6 .", ". . 6 . 7 . . 8 .")) is False
# assert sol.sudoku_solve(rows(". . 5 . . 2 . . .", ". . 9 . 4 7 . 2 .", ". . 8 . 5 6 . . 1", ". . . . . 8 3 4 .", ". . . . . . . . 6", ". . . . 3 . 1 8 .", ". 2 . . . . . . .", ". 9 . . 8 . 6 7 .", "3 . 6 5 7 . . . .")) is True
# assert sol.sudoku_solve(rows(". . 3 8 . . 4 . .", ". . . . 1 . . 7 .", ". 6 . . . 5 . . 9", ". . . 9 . . 6 . .", ". 2 . . . . . 1 .", ". . 4 . . 3 . . 2", ". . 2 . . . 8 . .", ". 1 . . . . . 5 .", "9 . . . . 7 . . 3")) is True
# assert sol.sudoku_solve(rows("1 1 . . . . . . .", *[". . . . . . . . ."] * 8)) is False
# assert sol.sudoku_solve(rows("1 . . . . . . . .", ". . . . . . . . .", ". . 1 . . . . . .", *[". . . . . . . . ."] * 6)) is False
# assert sol.sudoku_solve(rows("5 3 4 6 7 8 9 1 2", "6 7 2 1 9 5 3 4 8", "1 9 8 3 4 2 5 6 7", "8 5 9 7 6 1 4 2 3", "4 2 6 8 5 3 7 9 1", "7 1 3 9 2 4 8 5 6", "9 6 1 5 3 7 2 8 4", "2 8 7 4 1 9 6 3 5", "3 4 5 2 8 6 1 7 9")) is True
# assert sol.sudoku_solve(rows("5 3 4 6 7 8 9 1 2", "6 7 2 1 9 5 3 4 8", "1 9 8 3 4 2 5 6 7", "8 5 9 7 6 1 4 2 3", "4 2 6 8 5 3 7 9 1", "7 1 3 9 2 4 8 5 6", "9 6 1 5 3 7 2 8 4", "2 8 7 4 1 9 6 3 5", "3 4 5 2 8 6 1 7 .")) is True
# assert sol.sudoku_solve(rows("5 3 4 6 7 8 9 1 2", "6 7 2 1 9 5 3 4 8", "1 9 8 3 4 2 5 6 7", "8 5 9 7 6 1 4 2 3", "4 2 6 8 5 3 7 9 1", "7 1 3 9 2 4 8 5 6", "9 6 1 5 3 7 2 8 4", "2 8 7 4 1 9 6 3 5", "3 4 5 2 8 6 1 9 7")) is False
