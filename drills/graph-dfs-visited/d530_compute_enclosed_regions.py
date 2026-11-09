"""
EPI 18.3 Compute enclosed regions

Given a 2D list board of "B" and "W" characters, change to "B" every "W"
cell that cannot reach a border cell of the board through "W" cells,
moving between cells that share a side. Change board in place and return
nothing.

Example 1:

Input: board = [["B", "B", "B", "B", "B"],
                ["B", "W", "W", "B", "W"],
                ["B", "B", "W", "B", "W"],
                ["W", "B", "B", "B", "B"]]
Output: board becomes [["B", "B", "B", "B", "B"],
                       ["B", "B", "B", "B", "W"],
                       ["B", "B", "B", "B", "W"],
                       ["W", "B", "B", "B", "B"]]
Explanation: the cells (1, 1), (1, 2) and (2, 2) have no "W" path to the
border. The cells (1, 4), (2, 4) and (3, 0) are on the border.

Example 2:

Input: board = [["B", "B", "B"],
                ["B", "W", "B"],
                ["B", "W", "B"]]
Output: board does not change.
Explanation: the cell (1, 1) reaches the border cell (2, 1).

Constraints:

    1 <= len(board) <= 200
    1 <= len(board[0]) <= 200
    board[i][j] is "B" or "W".

    REQUIRED: O(rows * cols) time. NO recursion.
"""


class Solution:
    def fill_surrounded_regions(self, board: list[list[str]]) -> None:
        pass


sol = Solution()

board = [list(r) for r in ["BBBBB", "BWWBW", "BBWBW", "WBBBB"]]
sol.fill_surrounded_regions(board)
print(board)  # [['B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'W'], ['B', 'B', 'B', 'B', 'W'], ['W', 'B', 'B', 'B', 'B']]

# grid = lambda *rows: [list(r) for r in rows]
# board = grid("BBBBB", "BWWBW", "BBWBW", "WBBBB")
# sol.fill_surrounded_regions(board)
# assert board == grid("BBBBB", "BBBBW", "BBBBW", "WBBBB")
# board = grid("BBB", "BWB", "BWB")
# sol.fill_surrounded_regions(board)
# assert board == grid("BBB", "BWB", "BWB")
# board = grid("W")
# sol.fill_surrounded_regions(board)
# assert board == grid("W")
# board = grid("B")
# sol.fill_surrounded_regions(board)
# assert board == grid("B")
# board = grid("BBB", "BWB", "BBB")
# sol.fill_surrounded_regions(board)
# assert board == grid("BBB", "BBB", "BBB")
# board = grid("WWWW", "WWWW", "WWWW", "WWWW")
# sol.fill_surrounded_regions(board)
# assert board == grid("WWWW", "WWWW", "WWWW", "WWWW")
# board = grid("BBBBB", "BWWWB", "BWBWB", "BWWWB", "BBBBB")
# sol.fill_surrounded_regions(board)
# assert board == grid("BBBBB", "BBBBB", "BBBBB", "BBBBB", "BBBBB")
# board = grid("WWWWW", "WBBBW", "WBWBW", "WBBBW", "WWWWW")
# sol.fill_surrounded_regions(board)
# assert board == grid("WWWWW", "WBBBW", "WBBBW", "WBBBW", "WWWWW")
# board = grid("WBW")
# sol.fill_surrounded_regions(board)
# assert board == grid("WBW")
# board = grid("BWB", "WBW", "BWB")
# sol.fill_surrounded_regions(board)
# assert board == grid("BWB", "WBW", "BWB")
# board = [["B"] * 200] + [["B"] + ["W"] * 198 + ["B"] for _ in range(198)] + [["B"] * 200]
# sol.fill_surrounded_regions(board)
# assert board == [["B"] * 200 for _ in range(200)]
# snake = [["W" if 0 < i < 100 and 0 < j < 100 and (i % 2 == 1 or j == (99 if i % 4 == 2 else 1)) else "B" for j in range(101)] for i in range(101)]
# opened = [["W" if (i, j) == (0, 1) else v for j, v in enumerate(r)] for i, r in enumerate(snake)]
# board = [r[:] for r in opened]
# sol.fill_surrounded_regions(board)
# assert board == opened
# board = [r[:] for r in snake]
# sol.fill_surrounded_regions(board)
# assert board == [["B"] * 101 for _ in range(101)]
