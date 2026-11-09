"""
EPI 16.9 Pick up coins for maximum gain

Given a list coins of coin values in a row, two players take turns, and
you move first. On each turn the player takes the coin at either end of
the row. Both players play to make their own total as large as
possible. Return your total when the row is empty.

Example 1:

Input: coins = [5, 25, 10, 1]
Output: 26
Explanation: you take 1, which leaves [5, 25, 10]. The other player
takes 10 or 5, and you take 25. Taking the 5 first gives you at most 15.

Example 2:

Input: coins = [1, 100, 2]
Output: 3
Explanation: the other player always gets the 100.

Example 3:

Input: coins = [7]
Output: 7

Constraints:

    0 <= len(coins) <= 500
    0 <= coins[i] <= 1000

    REQUIRED: O(len(coins)^2) time and space. NO search over every
    sequence of turns.
"""


class Solution:
    def maximum_revenue(self, coins: list[int]) -> int:
        pass


sol = Solution()

print(sol.maximum_revenue([5, 25, 10, 1]))  # 26

# assert sol.maximum_revenue([5, 25, 10, 1]) == 26
# assert sol.maximum_revenue([1, 100, 2]) == 3
# assert sol.maximum_revenue([7]) == 7
# assert sol.maximum_revenue([]) == 0
# assert sol.maximum_revenue([3, 9]) == 9
# assert sol.maximum_revenue([10, 1, 1, 10]) == 11
# assert sol.maximum_revenue([2, 2, 2, 2]) == 4
# assert sol.maximum_revenue([8, 15, 3, 7]) == 22
# assert sol.maximum_revenue([1, 2, 3, 4, 5, 6]) == 12
# assert sol.maximum_revenue([20, 30, 2, 2, 2, 10]) == 42
# assert sol.maximum_revenue([1] * 499) == 250
# assert sol.maximum_revenue(list(range(1, 501))) == 62750
# assert sol.maximum_revenue([(i * 31) % 97 for i in range(500)]) == 12050
