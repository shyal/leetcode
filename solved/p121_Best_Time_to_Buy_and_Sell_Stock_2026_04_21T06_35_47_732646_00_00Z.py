"""
URL: https://leetcode.com/problems/best-time-to-buy-and-sell-stock/description/?envType=problem-list-v2&envId=vn57k9wr

121. Best Time to Buy and Sell Stock

You are given an array prices where prices[i] is the price of a given stock on the ith day.

You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.

Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.


Example 1:

Input: prices = [7,1,5,3,6,4]
Output: 5
Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5.
Note that buying on day 2 and selling on day 1 is not allowed because you must buy before you sell.

Example 2:

Input: prices = [7,6,4,3,1]
Output: 0
Explanation: In this case, no transactions are done and the max profit = 0.


Constraints:

    1 <= prices.length <= 10^5
    0 <= prices[i] <= 10^4


---

9
8
7
6
5         .
4       .   .
3     .       . . .
2 . .
1 
0 1 2 3 4 5 6 7 8 9


"""
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        _min = float('inf')
        _max = float('-inf')
        for p in prices:
            _min = min(_min, p)
            _max = max(_max, p - _min)
        return _max


sol = Solution()

# print(sol.maxProfit([7, 1, 5, 3, 6, 4]))  # 5

assert sol.maxProfit([7, 1, 5, 3, 6, 4]) == 5
assert sol.maxProfit([7, 6, 4, 3, 1]) == 0
assert sol.maxProfit([1]) == 0
assert sol.maxProfit([1, 2]) == 1
assert sol.maxProfit([2, 1]) == 0
assert sol.maxProfit([5, 5, 5, 5, 5]) == 0
assert sol.maxProfit([1, 2, 3, 4, 5]) == 4
assert sol.maxProfit([5, 4, 3, 2, 1]) == 0
assert sol.maxProfit([0, 0, 0, 0]) == 0
assert sol.maxProfit([0, 10000]) == 10000
assert sol.maxProfit([10000, 0]) == 0
assert sol.maxProfit([3, 2, 6, 5, 0, 3]) == 4
assert sol.maxProfit([2, 4, 1]) == 2
assert sol.maxProfit([1, 2, 1, 2]) == 1
assert sol.maxProfit([7, 1, 5, 3, 6, 4, 10]) == 9
assert sol.maxProfit([5, 1, 2, 3, 4, 0]) == 3
assert sol.maxProfit([10, 1, 10, 1, 10]) == 9
assert sol.maxProfit([0, 0, 0, 0, 1]) == 1
assert sol.maxProfit([1, 0, 0, 0, 0]) == 0
assert sol.maxProfit([2, 1, 2, 1, 0, 1, 2]) == 2