# REFERENCE: d516 EPI 16.9 Pick up coins for maximum gain
class Solution
  def maximum_revenue(coins: [int]) -> int
    n = len(coins)
    prefix = [0]
    for c in coins
      prefix <- prefix[-1] + c
    best = [0] * (n + 1)
    for j in 1..n
      for i in j - 1..0 by -1
        best[i] = prefix[j] - prefix[i] - min(best[i + 1], best[i])
    best[0]
