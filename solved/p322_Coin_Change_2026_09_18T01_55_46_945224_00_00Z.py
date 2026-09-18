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

Alright, so this still doesn't feel like solid ground.

        coins

      5   2   1

a  1  0   0   1
m  2  0   1   0
o  3  0   1   1

But let's look for a case where a greedy solution
wouldn't work.

assert sol.coinChange([1, 3, 4], 6) == 2


          coins

        1   3   4

a  1    1
m  2    2
o  3        1
u  4            1
n  5
t  6
s  7
   8
   9
   10
   11


hhmm let's try the other way


     0  1  2  3  4  5  6  7  8  9  10  11

1    0  1  2  3  4  5  6  7  8  9  10  11
3             1        2        3
4                1           2

nvm.

Learning.

LEETCODE: Accepted (365 ms, 19.8 MB)
"""


class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        dp = table(amount + 1)
        dp[0] = 0
        for a in range(1, amount + 1):
            candidates = [inf]
            for c in coins:
                if c <= a:
                    candidates.append(dp[a - c] + 1)
            dp[a] = min(candidates)
        return -1 if dp[amount] == inf else dp[amount]


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


# edge cases: one line each, the values are the reference solution's.
assert Solution().coinChange([1], 0) == 0  # single_coin_zero_amount
assert Solution().coinChange([2147483647], 10000) == -1  # only_coin_exceeds_amount
assert Solution().coinChange([2147483647], 0) == 0  # huge_coin_zero_amount
assert Solution().coinChange([1, 3, 4], 6) == 2  # largest_coin_first_costs_extra
assert (
    Solution().coinChange([1, 5, 10, 25], 30) == 2
)  # standard_denominations_greedy_exact
assert (
    Solution().coinChange([186, 419, 83, 408], 6249) == 20
)  # unsorted_coins_large_amount
assert (
    Solution().coinChange([9, 6, 5, 1], 11) == 2
)  # two_mid_coins_beat_largest_plus_ones
assert Solution().coinChange([4, 7], 15) == 3  # no_one_coin_exact_combo_only
assert Solution().coinChange([4, 7], 5) == -1  # no_one_coin_unreachable_small
assert (
    Solution().coinChange([3, 5, 6], 10000) == 1667
)  # sum_of_two_beats_largest_at_max_amount
assert (
    Solution().coinChange([5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], 100) == 20
)  # twelve_identical_coins
assert Solution().coinChange([2, 3], 7) == 3  # smallest_coin_alone_cannot_make_odd
