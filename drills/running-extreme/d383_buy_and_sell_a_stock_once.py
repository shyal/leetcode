"""
EPI 5.6 Buy and sell a stock once

Given a list of daily stock prices, return the largest profit from
buying the stock on a day and selling it on the same day or a later
day. Return 0 when no trade makes a profit.

Example 1:

Input: prices = [310, 315, 275, 295, 260, 270, 290, 230, 255, 250]
Output: 30
Explanation: Buy at 260 and sell at 290.

Example 2:

Input: prices = [7, 1, 5, 3, 6, 4]
Output: 5
Explanation: Buy at 1 and sell at 6.

Example 3:

Input: prices = [5, 4, 3]
Output: 0
Explanation: The price only goes down.

Constraints:

    0 <= len(prices) <= 10^5
    0 <= prices[i] <= 10^9

    REQUIRED: O(n) time, O(1) extra space.
"""


class Solution:
    def buy_and_sell_stock_once(self, prices: list[float]) -> float:
        pass


sol = Solution()

print(sol.buy_and_sell_stock_once([310, 315, 275, 295, 260, 270, 290, 230, 255, 250]))  # 30

# assert sol.buy_and_sell_stock_once([310, 315, 275, 295, 260, 270, 290, 230, 255, 250]) == 30
# assert sol.buy_and_sell_stock_once([7, 1, 5, 3, 6, 4]) == 5
# assert sol.buy_and_sell_stock_once([5, 4, 3]) == 0
# assert sol.buy_and_sell_stock_once([]) == 0
# assert sol.buy_and_sell_stock_once([5]) == 0
# assert sol.buy_and_sell_stock_once([1, 2]) == 1
# assert sol.buy_and_sell_stock_once([2, 1]) == 0
# assert sol.buy_and_sell_stock_once([3, 3, 3]) == 0
# assert sol.buy_and_sell_stock_once([1, 100]) == 99
# assert sol.buy_and_sell_stock_once([2, 4, 1, 7]) == 6
# assert sol.buy_and_sell_stock_once([9, 1, 9, 0, 5]) == 8
# assert sol.buy_and_sell_stock_once([1.5, 0.5, 2.25]) == 1.75
# assert sol.buy_and_sell_stock_once(list(range(10 ** 5))) == 99999
# assert sol.buy_and_sell_stock_once(list(range(10 ** 5, 0, -1))) == 0
# assert sol.buy_and_sell_stock_once([10 ** 9, 0] * 50000) == 10 ** 9
