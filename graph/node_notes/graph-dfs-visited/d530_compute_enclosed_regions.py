# REFERENCE: d530 EPI 18.3 Compute enclosed regions
class Solution:
    def fill_surrounded_regions(self, board):
        rows, cols = len(board), len(board[0])
        stack = [(r, c) for r in range(rows) for c in range(cols) if r in (0, rows - 1) or c in (0, cols - 1)]
        while stack:
            r, c = stack.pop()
            if 0 <= r < rows and 0 <= c < cols and board[r][c] == "W":
                board[r][c] = "T"
                stack += [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
        for row in board:
            row[:] = ["W" if v == "T" else "B" for v in row]
