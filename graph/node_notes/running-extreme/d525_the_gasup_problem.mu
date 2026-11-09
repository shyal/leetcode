# REFERENCE: d525 EPI 17.6 The gasup problem
class Solution
  def find_ample_city(gas: [int], dist: [int]) -> int
    tank, lowest = 0, 0
    ret city = 0
    for i in 0..<len(gas)
      tank += 20 * gas[i] - dist[i]
      if tank < lowest
        lowest, city = tank, i + 1
