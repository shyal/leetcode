# REFERENCE: d323 Knapsack
class Solution
  def knapsack(weights: [int], values: [int], capacity: int) -> int
    memo best(i, cap) =
      | i == len(weights) -> 0
      | weights[i] > cap  -> best(i + 1, cap)
      | else              -> max(best(i + 1, cap), values[i] + best(i + 1, cap - weights[i]))
    best(0, capacity)
