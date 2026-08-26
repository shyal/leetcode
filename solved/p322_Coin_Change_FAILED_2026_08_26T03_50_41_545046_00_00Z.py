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

Same issue as in 2025. I try to solve this using a naive div mod method, but
it's a DP solution. Failed.

"""


class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        n = 0
        coins.sort(reverse=True)
        for c in coins:
            div, mod = divmod(amount, c)
            n += div
            amount = mod
        return n if amount == 0 else -1


sol = Solution()

print(sol.coinChange([1, 2, 5], 11))  # 3

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


# FAILED: walked away after 6m 10s; no working solution.
# Judge the moves actually attempted as struggled, not clean.
