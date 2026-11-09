# REFERENCE: d483 EPI 13.10 Team photo day - 1
class Solution
  def valid_placement_exists(team0: [int], team1: [int]) -> bool
    all(a < b for a, b in zip(sort(team0), sort(team1)))
