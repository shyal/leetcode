# REFERENCE: d530 EPI 18.3 Compute enclosed regions
class Solution
  def fill_surrounded_regions(board: [[str]])
    stack = [p for p in cells(board, eq="W") if is_edge(board, p)]
    while stack
      p = stack .
      if board[p] == "W"
        board[p] = "T"
        stack += list(nbrs(board, p, eq="W"))
    for row in board
      row[:] = [v == "T" ? "W" : "B" for v in row]
