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

Greedy method fails on some test cases, due to "non-uniformity".

Looking at discussions for hints.

Hint:

> Take coins=[1,2,5] and amount = 11 as an example,
>
>     If I use one 1, I need to know the fewest number of coins I need to make up 10, i.e., dp[10]. Overall I need 1+dp[10] coins.
>     If I use one 2, I need 1+dp[9] coins.
>     If I use one 5, I need 1+dp[6] coins.
>
> Therefore, I need to calculate dp from 1 to amount.

yeahhh that doesn't help either. I'm going to look up the solution. I'm already glad i managed
to come up with the greedy solution.

Ok the optimial DP based solution didn't make sense.. so i turned it into a 2D problem,
using tabulate to see the coins needed for each value ranging from coin to amount,
for each denomination.

  coin    0  1    2    3    4    5    6    7    8    9    10
------  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ----
     1    0  1    2    3    4    5    6    7    8    9    10
     2    0       1         2         3         4         5
     3    0            1              2              3
     4    0                 1                   2
     5    0                      1                        2
     6    0                           1
     7    0                                1
     8    0                                     1
     9    0                                          1
    10    0                                               1
--------
0 1 1 1 1 1 1 1 1 1 1

Final result: 1

then we take the cummulative min.

Honestly this makes it so much easier undertanding what's going on.

"""


class Solution:

    def coinChangeGreedy(self, coins: List[int], amount: int) -> int:
        coins.sort(reverse=True)
        res = []
        for c in coins:
            if c <= amount:
                div, mod = divmod(amount, c)
                res.extend([c] * div)
                amount = mod
        return len(res) if amount == 0 else -1

    def coinChange(self, coins, amount):
        coins = sorted(coins)
        per_dp = []
        for _ in coins:
            row = [""] * (amount + 1)
            row[0] = 0
            per_dp.append(row)
        for i, coin in enumerate(coins):
            for x in range(coin, amount + 1):
                num_coins = per_dp[i][x - coin]
                if num_coins != "":
                    per_dp[i][x] = num_coins + 1

        # pretty printing
        table_data = [[coins[i]] + per_dp[i] for i in range(len(coins))]
        # print(tabulate(table_data, headers=["coin"] + list(range(amount + 1))))

        cum_dp = [maxsize] * (amount + 1)
        cum_dp[0] = 0
        for coin in coins:
            for x in range(coin, amount + 1):
                if cum_dp[x - coin] != maxsize:
                    cum_dp[x] = min(cum_dp[x], cum_dp[x - coin] + 1)

        # pretty printing
        # print("--------")
        # print(" ".join([str(v) if v != maxsize else "inf" for v in cum_dp]))

        return cum_dp[amount] if cum_dp[amount] != maxsize else -1


sol = Solution()
coins = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # Based on your output pattern
amount = 10
# print("\nFinal result:", sol.coinChange(coins, amount))

# print(sol.coinChange([1, 2], 0))
# print(sol.coinChange([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 10))

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
