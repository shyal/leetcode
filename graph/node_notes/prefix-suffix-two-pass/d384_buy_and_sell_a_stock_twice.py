# REFERENCE: d384 EPI 5.7 Buy and sell a stock twice
class Solution:
    def buy_and_sell_stock_twice(self, prices):
        n = len(prices)
        first = [0] * (n + 1)
        low = inf
        for i, p in enumerate(prices):
            low = min(low, p)
            first[i + 1] = max(first[i], p - low)
        best, high, second = 0, -inf, 0
        for i in reversed(range(n)):
            high = max(high, prices[i])
            second = max(second, high - prices[i])
            best = max(best, first[i] + second)
        return best
