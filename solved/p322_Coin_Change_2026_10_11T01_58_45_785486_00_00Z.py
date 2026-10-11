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

LEETCODE: Accepted (455 ms, 19.7 MB)
"""


# mu 0.7
# def coinChange(coins: [int], amount: int) -> int
#   dp = [0] + table(amount, fill=inf)
#   for a in 0..amount
#     for c in coins
#       if c <= a
#         dp[a] = min(dp[a], dp[a - c] + 1)
#   dp[-1] or -1 if inf

from math import inf


def table(*dims, fill=0):
    if len(dims) == 1:
        return [fill] * dims[0]
    if len(dims) == 2:
        return [[fill] * dims[1] for _ in range(dims[0])]
    return [table(*dims[1:], fill=fill) for _ in range(dims[0])]


class Solution:
    def coinChange(self, coins: list[int], amount: int) -> int:
        dp = [0] + table(amount, fill=inf)
        for a in range(0, amount + 1):
            for c in coins:
                if c <= a:
                    dp[a] = min(dp[a], dp[a - c] + 1)
        return (-1 if (_v := dp[-1]) == inf else _v)


sol = Solution()
print(sol.coinChange([1, 2, 5], 11))
_l, _r = sol.coinChange([1, 2, 5], 11), 3
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.coinChange([2], 3), -1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.coinChange([1], 0), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.coinChange([1], 1), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.coinChange([2, 2, 2], 4), 2
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.coinChange([1, 3, 4], 6), 2
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.coinChange([5], 3), -1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.coinChange([1, 2147483647], 2), 2
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.coinChange([1, 2, 5], 10000), 2000
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.coinChange([7, 14], 300), -1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.coinChange([1], 10000), 10000
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.coinChange([2, 5, 10, 1], 27), 4
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.coinChange([1, 2, 5], 0), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.coinChange([10], 10), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.coinChange([3, 7], 5), -1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = Solution().coinChange([1], 0), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = Solution().coinChange([2147483647], 10000), -1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = Solution().coinChange([2147483647], 0), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = Solution().coinChange([1, 3, 4], 6), 2
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = Solution().coinChange([1, 5, 10, 25], 30), 2
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = Solution().coinChange([186, 419, 83, 408], 6249), 20
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = Solution().coinChange([9, 6, 5, 1], 11), 2
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = Solution().coinChange([4, 7], 15), 3
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = Solution().coinChange([4, 7], 5), -1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = Solution().coinChange([3, 5, 6], 10000), 1667
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = Solution().coinChange([5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], 100), 20
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = Solution().coinChange([2, 3], 7), 3
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
