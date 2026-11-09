# REFERENCE: d517 EPI 16.10 Count the number of moves to climb stairs
class Solution
  def number_of_ways_to_top(top: int, maximum_step: int) -> int
    ways = [1]
    for h in 1..top
      ways <- sum(ways[max(0, h - maximum_step):h])
    ways[top]
