# REFERENCE: d513 EPI 16.6 The knapsack problem
class Solution
  def optimum_subject_to_capacity(items: [Item], capacity: int) -> int
    best = [0] * (capacity + 1)
    for item in items
      for c in capacity..item.weight by -1
        best[c] = max(best[c], best[c - item.weight] + item.value)
    best[capacity]
