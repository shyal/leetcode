"""
EPI 5.7 Buy and sell a stock twice

Given a list of daily stock prices, return the largest total profit
from at most two trades. A trade buys the stock on a day and sells it
on the same day or a later day. The second trade must buy on a day
after the first trade sells.

Example 1:

Input: prices = [12, 11, 13, 9, 12, 8, 14, 13, 15]
Output: 10
Explanation: Buy at 9 and sell at 12, then buy at 8 and sell at 15.

Example 2:

Input: prices = [1, 2, 3, 4, 5]
Output: 4
Explanation: A single trade from 1 to 5 is best. A second trade adds
nothing.

Example 3:

Input: prices = [7, 6, 4, 3, 1]
Output: 0

Constraints:

    0 <= len(prices) <= 10^5
    0 <= prices[i] <= 10^9

    REQUIRED: O(n) time.
"""


class Solution:
    def buy_and_sell_stock_twice(self, prices: list[float]) -> float:
        pass


sol = Solution()

print(sol.buy_and_sell_stock_twice([12, 11, 13, 9, 12, 8, 14, 13, 15]))  # 10

# assert sol.buy_and_sell_stock_twice([12, 11, 13, 9, 12, 8, 14, 13, 15]) == 10
# assert sol.buy_and_sell_stock_twice([1, 2, 3, 4, 5]) == 4
# assert sol.buy_and_sell_stock_twice([7, 6, 4, 3, 1]) == 0
# assert sol.buy_and_sell_stock_twice([]) == 0
# assert sol.buy_and_sell_stock_twice([5]) == 0
# assert sol.buy_and_sell_stock_twice([1, 2]) == 1
# assert sol.buy_and_sell_stock_twice([1, 5, 1, 5]) == 8
# assert sol.buy_and_sell_stock_twice([3, 3, 5, 0, 0, 3, 1, 4]) == 6
# assert sol.buy_and_sell_stock_twice([2, 1, 2, 0, 1]) == 2
# assert sol.buy_and_sell_stock_twice([1, 2, 4, 2, 5, 7, 2, 4, 9, 0]) == 13
# assert sol.buy_and_sell_stock_twice([310, 315, 275, 295, 260, 270, 290, 230, 255, 250]) == 55
# assert sol.buy_and_sell_stock_twice([1.5, 0.5, 2.25, 1.0, 2.0]) == 2.75
# assert sol.buy_and_sell_stock_twice(list(range(10 ** 5))) == 99999
# assert sol.buy_and_sell_stock_twice(list(range(10 ** 5, 0, -1))) == 0
# assert sol.buy_and_sell_stock_twice([0, 10 ** 9] * 50000) == 2 * 10 ** 9
# assert sol.buy_and_sell_stock_twice([i % 1000 for i in range(10 ** 5)]) == 1998
