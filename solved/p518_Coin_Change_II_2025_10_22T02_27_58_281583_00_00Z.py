"""
URL: https://leetcode.com/problems/coin-change-ii/description/

518. Coin Change II

You are given an integer array coins representing coins of different denominations and an integer amount representing a total amount of money.

Return the number of combinations that make up that amount. If that amount of money cannot be made up by any combination of the coins, return 0.

You may assume that you have an infinite number of each kind of coin.

The answer is guaranteed to fit into a signed 32-bit integer.


Example 1:

Input: amount = 5, coins = [1,2,5]
Output: 4
Explanation: there are four ways to make up the amount:
5=5
5=2+2+1
5=2+1+1+1
5=1+1+1+1+1

Example 2:

Input: amount = 3, coins = [2]
Output: 0
Explanation: the amount of 3 cannot be made up just with coins of 2.

Example 3:

Input: amount = 10, coins = [10]
Output: 1


Constraints:

        1 <= coins.length <= 300
        1 <= coins[i] <= 5000
        All the values of coins are unique.
        0 <= amount <= 5000
---

Hmm it still feels like i'm warming up to DP and the coin change problem, so this
extra twist of counting combos feels a bit of a stretch. For sure i can count
the combinations by simply computing all the subsets equal to amount, with repeats
however there are too many combinations, so this approach won't be efficient.

Let's try and think through this example

Input: amount = 5, coins = [1,2,5]
Output: 4
Explanation: there are four ways to make up the amount:
5=5
5=2+2+1
5=2+1+1+1
5=1+1+1+1+1

So one approach here is to sort the coins, to start with small denomiations,
in the case of 1, it gives us 1 way of adding up to 5.

In the case of 2, we're taking the number of ways for `1`, and subtracting 2, which is
another way, then 4, which is yet another way.

In the case of 5, it's already our target amount, so cannot compute combinations.

class Solution:
    def change(self, amount: int, coins: List[int]) -> int:
        coins.sort()

        @cache
        def dp(coinIndex, amount):
            if amount == 0:
                return 0
            val = coins[coinIndex]
            if coins[coinIndex] == 1:
                return 1
            div, mod = divmod(amount, val)
            ways = 1
            if div:
                for i in range(1, div + 1):
                    ways += dp(coinIndex - 1, amount - (val * i))
            return ways

        _5 = dp(2, amount)
        return _5

Out of time. I give up. Will have to look up the solution.

"""


class Solution:
    def change(self, amount: int, coins: List[int]) -> int:
        """
        Not my solution
        https://leetcode.com/problems/coin-change-ii/solutions/3892702/100-dynamic-programming-video-optimal-solution/
        """
        dp = [0] * (amount + 1)
        dp[0] = 1

        for coin in coins:
            for j in range(coin, amount + 1):
                dp[j] += dp[j - coin]

        return dp[amount]


sol = Solution()
res = sol.change(amount=5, coins=[1, 2, 5])
# print(res)
# assert res == 4
