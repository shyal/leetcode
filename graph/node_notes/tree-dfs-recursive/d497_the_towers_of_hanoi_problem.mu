# REFERENCE: d497 EPI 15.1 The Towers of Hanoi problem
class Solution
  def compute_tower_hanoi(num_rings: int) -> [[int]]
    ret moves = []
    def transfer(n, src, dst, via)
      if n
        transfer(n - 1, src, via, dst)
        moves <- [src, dst]
        transfer(n - 1, via, dst, src)
    transfer(num_rings, 0, 1, 2)
