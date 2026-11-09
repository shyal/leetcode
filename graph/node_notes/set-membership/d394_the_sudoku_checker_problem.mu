# REFERENCE: d394 EPI 5.17 The Sudoku checker problem
class Solution
  def is_valid_sudoku(partial_assignment: [[int]]) -> bool
    seen = set()
    for >i, row in partial_assignment
      for >j, d in row
        if d
          for key in (("row", i, d), ("col", j, d), ("box", i // 3, j // 3, d))
            if key in seen
              return false
            seen.add(key)
    true
