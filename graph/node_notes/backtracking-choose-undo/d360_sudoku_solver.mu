# REFERENCE: d360 Sudoku Solver
class Solution
  def sudoku_solve(board: [[str]]) -> bool
    rows = [set() for _ in 0..<9]
    cols = [set() for _ in 0..<9]
    boxes = [set() for _ in 0..<9]
    def box(i, j)
      i // 3 * 3 + j // 3
    def free(i, j, c)
      c not in rows[i] and c not in cols[j] and c not in boxes[box(i, j)]
    def place(i, j, c)
      rows[i].add(c)
      cols[j].add(c)
      boxes[box(i, j)].add(c)
      board[i][j] = c
    def lift(i, j, c)
      rows[i].remove(c)
      cols[j].remove(c)
      boxes[box(i, j)].remove(c)
      board[i][j] = "."
    blanks = []
    for i in 0..<9
      for j in 0..<9
        c = board[i][j]
        if c == "."
          blanks <- (i, j)
        elif not free(i, j, c)
          return false
        else
          place(i, j, c)
    def fill(k)
      if k == len(blanks)
        return true
      r, col = blanks[k]
      for d in "123456789"
        if free(r, col, d)
          place(r, col, d)
          if fill(k + 1)
            return true
          lift(r, col, d)
      false
    fill(0)
