"""
URL: https://leetcode.com/problems/cells-in-a-range-on-an-excel-sheet/description/

2194. Cells in a Range on an Excel Sheet

A cell (r, c) of an excel sheet is represented as a string "<col><row>" where:

<col> denotes the column number c of the cell. It is represented by alphabetical letters.
For example, the 1st column is denoted by 'A', the 2nd by 'B', the 3rd by 'C', and so on.

<row> is the row number r of the cell. The rth row is represented by the integer r.

You are given a string s in the format "<col1><row1>:<col2><row2>", where <col1> represents the column c1, <row1> represents the row r1, <col2> represents the column c2, and <row2> represents the row r2, such that r1 <= r2 and c1 <= c2.

Return the list of cells (x, y) such that col1 <= x <= col2 and row1 <= y <= row2. The cells should be represented as a string in the same format as they are represented in the excel sheet and should be returned sorted by column then by row (from top-left to bottom-right cell).


Example 1:

Input: s = "K1:L2"
Output: ["K1","K2","L1","L2"]
Explanation: The above diagram shows the cells which should be present in the list. The red arrows denote the order in which the cells are returned.

Example 2:

Input: s = "A1:F1"
Output: ["A1","B1","C1","D1","E1","F1"]
Explanation: The above diagram shows the cells which should be present in the list. The red arrow denotes the order in which the cells are returned.

Constraints:

    s.length == 5
    'A' <= s[0] <= s[3] <= 'Z'
    '1' <= s[1] <= s[4] <= '9'
    s consists of uppercase English letters, digits and ':'.

"""


class Solution:
    def cellsInRange(self, s: str) -> List[str]:
        start_col, start_row, _, end_col, end_row = list(s)
        start_col_index = ascii_uppercase.index(start_col)
        end_col_index = ascii_uppercase.index(end_col)
        letters = ascii_uppercase[start_col_index : end_col_index + 1]
        numbers = list(range(int(start_row), int(end_row) + 1))
        res = [*product(letters, numbers)]
        return ["".join(str(y) for y in x) for x in res]


sol = Solution()

# print(sol.cellsInRange("K1:L2"))  # ["K1","K2","L1","L2"]
# print(sol.cellsInRange("A1:Z1"))

assert sol.cellsInRange("K1:L2") == ["K1", "K2", "L1", "L2"]
assert sol.cellsInRange("A1:F1") == ["A1", "B1", "C1", "D1", "E1", "F1"]
assert sol.cellsInRange("A1:A1") == ["A1"]
assert sol.cellsInRange("Z9:Z9") == ["Z9"]
assert sol.cellsInRange("A1:A9") == [
    "A1",
    "A2",
    "A3",
    "A4",
    "A5",
    "A6",
    "A7",
    "A8",
    "A9",
]
assert sol.cellsInRange("X9:Z9") == ["X9", "Y9", "Z9"]
assert sol.cellsInRange("C3:E5") == [
    "C3",
    "C4",
    "C5",
    "D3",
    "D4",
    "D5",
    "E3",
    "E4",
    "E5",
]
assert sol.cellsInRange("A1:Z1") == [
    "A1",
    "B1",
    "C1",
    "D1",
    "E1",
    "F1",
    "G1",
    "H1",
    "I1",
    "J1",
    "K1",
    "L1",
    "M1",
    "N1",
    "O1",
    "P1",
    "Q1",
    "R1",
    "S1",
    "T1",
    "U1",
    "V1",
    "W1",
    "X1",
    "Y1",
    "Z1",
]
assert sol.cellsInRange("Y1:Z2") == ["Y1", "Y2", "Z1", "Z2"]
