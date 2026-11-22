# You are given an array prices where prices[i] is the price of a given
# stock on the ith day, and an integer fee representing a transaction fee.
#
# Find the maximum profit you can achieve. You may complete as many
# transactions as you like, but you need to pay the transaction fee for
# each transaction.
#
# Note:
#
#     You may not engage in multiple transactions simultaneously (i.e.,
#     you must sell the stock before you buy again).
#     The transaction fee is only charged once for each stock purchase
#     and sale.
#
# Example 1:
#
# Input: prices = [1, 3, 2, 8, 4, 9], fee = 2
# Output: 8
# Explanation: The maximum profit can be achieved by:
# - Buying at prices[0] = 1
# - Selling at prices[3] = 8
# - Buying at prices[4] = 4
# - Selling at prices[5] = 9
# The total profit is ((8 - 1) - 2) + ((9 - 4) - 2) = 8.
#
# Example 2:
#
# Input: prices = [1, 3, 7, 5, 10, 3], fee = 3
# Output: 6
#
# Constraints:
#
#     1 <= prices.length <= 5 * 10^4
#     1 <= prices[i] < 5 * 10^4
#     0 <= fee < 5 * 10^4
#
#     REQUIRED: O(n) time.
#
# ---
# learning
# mu 0.20

class Solution
  def maxProfit(prices: [int], fee: int) -> int
    n = len prices
    memo {
      i -> i == n: 0, 0
        (max(c, h - prices[i]), max(h, c + prices[i] - fee)) = mu(i + 1)
    }(0)[0]

sol = Solution()

print(sol.maxProfit([1, 3, 2, 8, 4, 9], 2))  # 8

assert sol.maxProfit([1, 3, 2, 8, 4, 9], 2) == 8
assert sol.maxProfit([1, 3, 7, 5, 10, 3], 3) == 6
assert sol.maxProfit([5], 1) == 0
assert sol.maxProfit([1, 5], 0) == 4
assert sol.maxProfit([1, 5], 4) == 0
assert sol.maxProfit([1, 5], 10) == 0
assert sol.maxProfit([9, 7, 4, 1], 0) == 0
assert sol.maxProfit([1, 2, 3, 4, 5], 0) == 4
assert sol.maxProfit([1, 2, 3, 4, 5], 1) == 3
assert sol.maxProfit([1, 4, 2, 5], 0) == 6
assert sol.maxProfit([1, 4, 2, 5], 1) == 4
assert sol.maxProfit([1, 4, 2, 5], 2) == 2
assert sol.maxProfit([2, 1, 4, 4, 2, 3, 2, 5, 1, 2], 1) == 4
assert sol.maxProfit([4, 5, 2, 4, 3, 3, 1, 2, 5, 4], 1) == 4
assert sol.maxProfit([1, 3] * 25000, 2) == 0
assert sol.maxProfit([1, 4] * 25000, 2) == 25000
assert sol.maxProfit(list(1..<50000), 3) == 49995
