# REFERENCE: d499 EPI 15.3 Generate all nonattacking placements of n-Queens
class Solution
  def n_queens(n: int) -> [[int]]
    ret out, cols = []..
    used, up, down = set(), set(), set()
    def place(r)
      if r == n
        out <- cols[:]
        return
      for c in 0..<n
        if c in used or r + c in up or r - c in down
          continue
        used.add(c)
        up.add(r + c)
        down.add(r - c)
        cols <- c
        place(r + 1)
        cols .
        used.remove(c)
        up.remove(r + c)
        down.remove(r - c)
    place(0)
