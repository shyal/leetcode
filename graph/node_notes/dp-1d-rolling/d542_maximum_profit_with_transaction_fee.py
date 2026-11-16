# REFERENCE: d542 Maximum Profit With Transaction Fee
class Solution:
    def maxProfit(self, prices, fee):
        cash, hold = 0, -prices[0]
        for p in prices[1:]:
            cash = max(cash, hold + p - fee)
            hold = max(hold, cash - p)
        return cash
