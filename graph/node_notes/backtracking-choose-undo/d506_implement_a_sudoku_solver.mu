# REFERENCE: d506 EPI 15.10 Implement a Sudoku solver
class Solution
  def solve_sudoku(partial_assignment: [[int]]) -> bool
    board = partial_assignment
    rows = [set() for _ in 0..<9]
    cols = [set() for _ in 0..<9]
    boxes = [set() for _ in 0..<9]
    blanks = []
    for i in 0..<9
      for j in 0..<9
        d = board[i][j]
        if d == 0
          blanks <- (i, j)
          continue
        b = i // 3 * 3 + j // 3
        if d in rows[i] or d in cols[j] or d in boxes[b]
          return false
        rows[i].add(d)
        cols[j].add(d)
        boxes[b].add(d)
    def fill(k)
      if k == len(blanks)
        return true
      r, c = blanks[k]
      box = r // 3 * 3 + c // 3
      for digit in 1..9
        if digit in rows[r] or digit in cols[c] or digit in boxes[box]
          continue
        rows[r].add(digit)
        cols[c].add(digit)
        boxes[box].add(digit)
        board[r][c] = digit
        if fill(k + 1)
          return true
        board[r][c] = 0
        rows[r].remove(digit)
        cols[c].remove(digit)
        boxes[box].remove(digit)
      false
    fill(0)
