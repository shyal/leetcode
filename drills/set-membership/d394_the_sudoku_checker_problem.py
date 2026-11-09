"""
EPI 5.17 The Sudoku checker problem

Given a 9 x 9 grid partial_assignment of integers from 0 to 9, return
True if no row, no column and no 3 x 3 subgrid holds the same digit
twice, and False if not. The value 0 marks an empty cell and never
counts as a repeat. The grid does not have to be solvable.

The nine 3 x 3 subgrids are the rows 0-2, 3-5 and 6-8 crossed with the
columns 0-2, 3-5 and 6-8.

Example 1:

Input: partial_assignment =
    5 3 0 | 0 7 0 | 0 0 0
    6 0 0 | 1 9 5 | 0 0 0
    0 9 8 | 0 0 0 | 0 6 0
    ------+-------+------
    8 0 0 | 0 6 0 | 0 0 3
    4 0 0 | 8 0 3 | 0 0 1
    7 0 0 | 0 2 0 | 0 0 6
    ------+-------+------
    0 6 0 | 0 0 0 | 2 8 0
    0 0 0 | 4 1 9 | 0 0 5
    0 0 0 | 0 8 0 | 0 7 9
Output: True

Example 2:

Input: the grid of Example 1 with 8 at row 0, column 0 instead of 5
Output: False
Explanation: Column 0 holds 8 twice, at rows 0 and 3. The top-left
subgrid also holds 8 twice.

Example 3:

Input: a grid of 81 zeros
Output: True

Constraints:

    len(partial_assignment) == 9
    len(partial_assignment[i]) == 9
    0 <= partial_assignment[i][j] <= 9

    REQUIRED: O(n^2) time, where n = 9 is the side of the grid.
"""


class Solution:
    def is_valid_sudoku(self, partial_assignment: list[list[int]]) -> bool:
        pass


sol = Solution()


def grid(lines):
    return [[int(c) for c in line.split()] for line in lines]


def placed(cells):
    g = [[0] * 9 for _ in range(9)]
    for i, j, d in cells:
        g[i][j] = d
    return g


example = grid([
    "5 3 0 0 7 0 0 0 0",
    "6 0 0 1 9 5 0 0 0",
    "0 9 8 0 0 0 0 6 0",
    "8 0 0 0 6 0 0 0 3",
    "4 0 0 8 0 3 0 0 1",
    "7 0 0 0 2 0 0 0 6",
    "0 6 0 0 0 0 2 8 0",
    "0 0 0 4 1 9 0 0 5",
    "0 0 0 0 8 0 0 7 9",
])

print(sol.is_valid_sudoku(example))  # True

# assert sol.is_valid_sudoku(example) is True
# assert sol.is_valid_sudoku([[8] + example[0][1:]] + example[1:]) is False
# assert sol.is_valid_sudoku(placed([])) is True
# assert sol.is_valid_sudoku(placed([(4, 4, 9)])) is True
# assert sol.is_valid_sudoku(placed([(0, 0, 1), (0, 8, 1)])) is False
# assert sol.is_valid_sudoku(placed([(0, 4, 7), (8, 4, 7)])) is False
# assert sol.is_valid_sudoku(placed([(0, 0, 2), (1, 1, 2)])) is False
# assert sol.is_valid_sudoku(placed([(7, 7, 3), (8, 8, 3)])) is False
# assert sol.is_valid_sudoku(placed([(0, 0, 2), (1, 3, 2), (2, 6, 2)])) is True
# assert sol.is_valid_sudoku(placed([(0, 2, 5), (0, 3, 5)])) is False
# assert sol.is_valid_sudoku(placed([(2, 0, 4), (3, 0, 4)])) is False
# assert sol.is_valid_sudoku([[(3 * i + i // 3 + j) % 9 + 1 for j in range(9)] for i in range(9)]) is True
# assert sol.is_valid_sudoku([[(i + j) % 9 + 1 for j in range(9)] for i in range(9)]) is False
# assert sol.is_valid_sudoku([[j + 1 for j in range(9)] for i in range(9)]) is False
