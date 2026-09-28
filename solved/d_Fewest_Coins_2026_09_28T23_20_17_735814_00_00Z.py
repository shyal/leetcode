"""
DRILL: Fewest Coins
TRAINS: dp-1d-rolling

Given a list coins of coin values and an integer amount, return the fewest
coins whose values add up to amount, or -1 when no choice of coins does. A
coin value may be used any number of times.

Example 1:

Input: coins = [1, 3, 4], amount = 6
Output: 2
Explanation: 3 + 3. Taking the largest coin first gives 4 + 1 + 1, three coins.

Example 2:

Input: coins = [1, 2, 5], amount = 11
Output: 3
Explanation: 5 + 5 + 1.

Example 3:

Input: coins = [2], amount = 3
Output: -1

Constraints:

    1 <= len(coins) <= 12
    1 <= coins[i] <= 2^31 - 1
    0 <= amount <= 10^4

    REQUIRED: O(amount * len(coins)) time, one table entry per amount from 0
    to amount, each built from smaller amounts. NO largest-coin-first; NO
    divmod.
"""


# mu 0.6
# def fewestCoins(coins: [int], amount: int) -> int
#   dp = table(amount + 1, fill=inf)
#   dp[0] = 0
#   for a in range(1, amount + 1)
#       dp[a] = min((dp[a - c] + 1 for c in coins if c <= a), default=inf)
#   return -1 if dp[amount] == inf else dp[amount]

from math import inf


def table(*dims, fill=0):
    if len(dims) == 1:
        return [fill] * dims[0]
    if len(dims) == 2:
        return [[fill] * dims[1] for _ in range(dims[0])]
    return [table(*dims[1:], fill=fill) for _ in range(dims[0])]


class Solution:
    def fewestCoins(self, coins: list[int], amount: int) -> int:
        dp = table(amount + 1, fill=inf)
        dp[0] = 0
        for a in range(1, amount + 1):
            dp[a] = min((dp[a - c] + 1 for c in coins if c <= a), default=inf)
        return -1 if dp[amount] == inf else dp[amount]


sol = Solution()
print(sol.fewestCoins([1, 3, 4], 6))
