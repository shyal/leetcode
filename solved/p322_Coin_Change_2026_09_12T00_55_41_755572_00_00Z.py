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

This isn't a greedy problem. It's a DP problem.

We need to list all the coin combos and pick the shortest path.. just can't remember how.

11 -> 3
because 5, 5, 1

We need to think of a case where the greedy approach fails.



[2, 5, 10, 1], 27

10, 1, 5, 2

greedy works


[1, 3, 4], 6

3, 3

Ok here greedy fails.. because it would have resulted in 4, 1, 1 which is more coins than 3, 3

So if we think of the number of coins to make the result, we get:

1 1 1 1 1 1 -> 6
3 3 -> 6
4 1 1 -> 6

Maybe a dp table like

    4     3      1     num coins
1   1     x      2 ->     3
2   x     2        ->     2
3   x     x      2 ->     6

So this seems to work.. create a DP table, where the rows represent the
number of coins being used, and the columns represent the denomination.

Do a divmod, so for row 0, divmod(6, 4) = 1 rem 2. So we mark the 1, and carry the 2.
Then divmod(2, 3) = 0, rem 2
Then divmod(2, 1) = 2, rem 0

over time! But solved it.

"""


class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        DP = []
        coins.sort(reverse=True)
        for _ in range(1, amount):
            DP.append([0] * len(coins))

        if amount == 0:
            return 0

        res = float("inf")

        print(coins)
        print("---")

        for i, num_coins in enumerate(range(1, amount)):
            change = amount
            num = 0
            for j, coin in enumerate(coins):
                d, change = divmod(change, coin * num_coins)
                DP[i][j] = d * num_coins
                num += d * num_coins
            if num != 0 and change == 0 and num < res:
                res = num
            print(DP[i])
        return res if res != float("inf") else -1


sol = Solution()

print(sol.coinChange([1, 3, 4], 6))


print(sol.coinChange([1, 2, 5], 11))  # 3

assert sol.coinChange([1, 2, 5], 11) == 3
assert sol.coinChange([2], 3) == -1
assert sol.coinChange([1], 0) == 0

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
