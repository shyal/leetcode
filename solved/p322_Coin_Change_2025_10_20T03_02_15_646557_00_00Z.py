"""
URL: https://leetcode.com/problems/coin-change/description/

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
        1 <= coins[i] <= 231 - 1
        0 <= amount <= 104

---

Makes a lot more sense, but should reschedule in a week or so.
"""


class Solution:

    def coinChange(self, coins, amount):
        cum_dp = [0] + [maxsize] * amount
        for coin in coins:
            for x in range(coin, amount + 1):
                cum_dp[x] = min(cum_dp[x], cum_dp[x - coin] + 1)
        return cum_dp[amount] if cum_dp[amount] != maxsize else -1


sol = Solution()

res = sol.coinChange(coins=[186, 419, 83, 408], amount=6249)
assert res == 20

res = sol.coinChange(coins=[1, 2, 5, 10, 100, 1000], amount=1101)
assert res == 3

res = sol.coinChange(coins=[1, 2, 5], amount=11)
assert res == 3

res = sol.coinChange(coins=[2], amount=3)
assert res == -1

res = sol.coinChange(coins=[1], amount=0)
assert res == 0
