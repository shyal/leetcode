"""
URL: https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/description/?envType=problem-list-v2&envId=vn57k9wr

122. Best Time to Buy and Sell Stock II

You are given an integer array prices where prices[i] is the price of a given stock on the iᵗʰ day.

On each day, you may decide to buy and/or sell the stock. You can only hold at most one share of the stock at any time. However, you can sell and buy the stock multiple times on the same day, ensuring you never hold more than one share of the stock.

Find and return the maximum profit you can achieve.

Example 1:

Input: prices = [7,1,5,3,6,4]
Output: 7
Explanation: Buy on day 2 (price = 1) and sell on day 3 (price = 5), profit = 5-1 = 4.
Then buy on day 4 (price = 3) and sell on day 5 (price = 6), profit = 6-3 = 3.
Total profit is 4 + 3 = 7.

Example 2:

Input: prices = [1,2,3,4,5]
Output: 4
Explanation: Buy on day 1 (price = 1) and sell on day 5 (price = 5), profit = 5-1 = 4.
Total profit is 4.

Example 3:

Input: prices = [7,6,4,3,1]
Output: 0
Explanation: There is no way to make a positive profit, so we never buy the stock to achieve the maximum profit of 0.

Constraints:

    1 <= prices.length <= 3 * 10^4
    0 <= prices[i] <= 10^4
---
prices = [7,1,5,3,6,4]



7 x
6                                x sell
5                x sell
4                                            x
3                        x buy
2
1        x buy
          
  1      2       3       4       5           6

A strategy might be to look for changes in direction, and buy before price turns positive, and sell before it turns negative

7 
6 
5 
4 
3 
2
1
          
  1      2       3       4       5           6

LEETCODE: Accepted (3 ms, 20.3 MB)
"""


# mu 0.7
# def maxProfit(prices: [int]) -> int
#   profit = 0
#   holding = -1
#   for i, (price, next_price) in zip(prices, prices[1:])
#     # print(i)
#     if next_price == price
#       # print("flat")
#       pass
#     elif next_price > price
#       if holding == -1
#         holding = prices[i]
#       # print('buy')
#     else
#       if holding != -1
#         # print('sell')
#         profit += price - holding
#         holding = -1
#   if holding != -1
#     # print('sell')
#     profit += next_price - holding
#   profit

class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        profit = 0
        holding = -1
        for i, (price, next_price) in enumerate(zip(prices, prices[1:])):
            if next_price == price:
                pass
            elif next_price > price:
                if holding == -1:
                    holding = prices[i]
            else:
                if holding != -1:
                    profit += price - holding
                    holding = -1
        if holding != -1:
            profit += next_price - holding
        return profit


sol = Solution()
print(sol.maxProfit([7, 1, 5, 3, 6, 4]))
_l, _r = sol.maxProfit([7, 1, 5, 3, 6, 4]), 7
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxProfit([1, 2, 3, 4, 5]), 4
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxProfit([7, 6, 4, 3, 1]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxProfit([0]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxProfit([10000]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxProfit([1, 1, 1, 1, 1]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxProfit([5, 5, 5, 5, 5, 5, 5]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxProfit([1, 2, 1, 2, 1, 2, 1, 2]), 4
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxProfit([10, 9, 8, 7, 6, 5, 4, 3, 2, 1]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxProfit([1, 10000, 1, 10000, 1, 10000]), 29997
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxProfit([0, 0, 0, 0, 0, 0, 0]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxProfit([10000, 0, 10000, 0, 10000]), 20000
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxProfit([1] * 30000), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxProfit(list(range(0, 30000))), 29999
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxProfit(list(range(30000, 0, -1))), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
