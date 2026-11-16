# REFERENCE: d542 Maximum Profit With Transaction Fee
class Solution
  def maxProfit(prices: [int], fee: int) -> int
    cash, hold = 0, -prices[0]
    for p in prices[1:]
      cash = max(cash, hold + p - fee)
      hold = max(hold, cash - p)
    cash
