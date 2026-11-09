# REFERENCE: d383 EPI 5.6 Buy and sell a stock once
class Solution
  def buy_and_sell_stock_once(prices: [float]) -> float
    low, best = inf, 0
    for p in prices
      low = min(low, p)
      best = max(best, p - low)
    best
