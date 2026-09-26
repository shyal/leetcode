"""
URL: https://leetcode.com/problems/coin-change/description/?envType=problem-list-v2&envId=vn57k9wr

322. Coin Change

You are given an integer array coins representing coins of different denominations and an integer amount representing a total amount of money.

Return the fewest number of coins that you need to make up that amount. If that amount of money cannot be made up by any combination of the coins, return -1.

You may assume that you have an infinite number of each kind of coin.

Example 1:

Input: coins = [1,2,5], amount = 11
Output: 3
Explanation: 11 = 5 + 5 + 1

Example 2:

Input: coins = [2], amount = 3
Output: -1

Example 3:

Input: coins = [1], amount = 0
Output: 0

Constraints:

    1 <= coins.length <= 12
    1 <= coins[i] <= 2^31 - 1
    0 <= amount <= 10^4
---
so we need to figure out how many coins of which types
are needed, for every amount, and use dp

so for an amount of 0, we need 0 coins
for an amount of 1, we need one coin
for an amount of 2, we need to decide whether
to use a `2` coin, or whether to use the amount
of coins for current amount - coin, i think

Got stuck here.

def coinChange(coins: [int], amount: int) -> int
  ret dp = table(amount + 1)
  for i, a in range(amount + 1)
    options = []
    for c in coins
      if c == a
        options <- c
      elif c < a and a - c >= 0
        options <- dp[a - c]
    print('amount', a, 'options:', options)
    dp[i] = min(options) if options else 0

looking at notes from previous solve.

Learning......

LEETCODE: Accepted (432 ms, 19.7 MB)
"""


# mu 0.5
# def coinChange(coins: [int], amount: int) -> int
#   dp = table(amount + 1)
#   dp[0] = 0
#   for a in range(1, amount + 1)
#     options = [inf]
#     for c in coins
#       if c <= a
#         options <- dp[a - c] + 1
#     dp[a] = min(options)
#   -1 if dp[amount] == inf else dp[amount]
#

from math import inf


def table(*dims, fill=0):
    if len(dims) == 1:
        return [fill] * dims[0]
    if len(dims) == 2:
        return [[fill] * dims[1] for _ in range(dims[0])]
    return [table(*dims[1:], fill=fill) for _ in range(dims[0])]


class Solution:
    def coinChange(self, coins: list[int], amount: int) -> int:
        dp = table(amount + 1)
        dp[0] = 0
        for a in range(1, amount + 1):
            options = [inf]
            for c in coins:
                if c <= a:
                    options.append(dp[a - c] + 1)
            dp[a] = min(options)
        return -1 if dp[amount] == inf else dp[amount]


sol = Solution()
print(sol.coinChange([1, 2, 5], 11))
assert sol.coinChange([1, 2, 5], 11) == 3
assert sol.coinChange([2], 3) == -1
assert sol.coinChange([1], 0) == 0
assert sol.coinChange([1], 1) == 1
assert sol.coinChange([2, 2, 2], 4) == 2
assert sol.coinChange([1, 3, 4], 6) == 2
assert sol.coinChange([5], 3) == -1
assert sol.coinChange([1, 2147483647], 2) == 2
assert sol.coinChange([1, 2, 5], 10000) == 2000
assert sol.coinChange([7, 14], 300) == -1
assert sol.coinChange([1], 10000) == 10000
assert sol.coinChange([2, 5, 10, 1], 27) == 4
assert sol.coinChange([1, 2, 5], 0) == 0
assert sol.coinChange([10], 10) == 1
assert sol.coinChange([3, 7], 5) == -1
assert Solution().coinChange([1], 0) == 0
assert Solution().coinChange([2147483647], 10000) == -1
assert Solution().coinChange([2147483647], 0) == 0
assert Solution().coinChange([1, 3, 4], 6) == 2
assert Solution().coinChange([1, 5, 10, 25], 30) == 2
assert Solution().coinChange([186, 419, 83, 408], 6249) == 20
assert Solution().coinChange([9, 6, 5, 1], 11) == 2
assert Solution().coinChange([4, 7], 15) == 3
assert Solution().coinChange([4, 7], 5) == -1
assert Solution().coinChange([3, 5, 6], 10000) == 1667
assert Solution().coinChange([5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], 100) == 20
assert Solution().coinChange([2, 3], 7) == 3
