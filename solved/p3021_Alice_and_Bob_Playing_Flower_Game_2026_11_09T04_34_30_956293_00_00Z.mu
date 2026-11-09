# URL: https://leetcode.com/problems/alice-and-bob-playing-flower-game/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 3021. Alice and Bob Playing Flower Game
#
# Alice and Bob are playing a turn-based game on a field, with two lanes of flowers between them. There are x flowers in the first lane between Alice and Bob, and y flowers in the second lane between them.
#
# The game proceeds as follows:
#
# 1. Alice takes the first turn.
# 2. In each turn, a player must choose either one of the lanes and pick one flower from that side.
# 3. At the end of the turn, if there are no flowers left at all in either lane, the current player captures their opponent and wins the game.
#
# Given two integers, n and m, the task is to compute the number of possible pairs (x, y) that satisfy the conditions:
#
# - Alice must win the game according to the described rules.
# - The number of flowers x in the first lane must be in the range [1, n].
# - The number of flowers y in the second lane must be in the range [1, m].
#
# Return the number of possible pairs (x, y) that satisfy the conditions mentioned in the statement.
#
# Example 1:
#
# Input: n = 3, m = 2
# Output: 3
# Explanation: The following pairs satisfy conditions described in the statement: (1,2), (3,2), (2,1).
#
# Example 2:
#
# Input: n = 1, m = 1
# Output: 0
# Explanation: No pairs satisfy the conditions described in the statement.
#
# Constraints:
#
#     1 <= n, m <= 10^5
#
# ---
# LEETCODE: Accepted (129 ms, 19.4 MB)

# mu 0.16

class Solution
  def flowerGame(n: int, m: int) -> int
    x_even = count for x in 1..n: x is even
    x_odd = count for x in 1..n: x is odd
    y_even = count for x in 1..m: x is even
    y_odd = count for x in 1..m: x is odd
    x_even * y_odd + x_odd * y_even

sol = Solution()

print(sol.flowerGame(3, 2))  # 3

assert sol.flowerGame(3, 2) == 3
assert sol.flowerGame(1, 1) == 0

assert sol.flowerGame(1, 100000) == 50000
assert sol.flowerGame(100000, 1) == 50000
assert sol.flowerGame(100000, 100000) == 5000000000
assert sol.flowerGame(2, 2) == 2
assert sol.flowerGame(2, 3) == 3
assert sol.flowerGame(3, 3) == 4
assert sol.flowerGame(1, 2) == 1
assert sol.flowerGame(2, 1) == 1
assert sol.flowerGame(99999, 100000) == 4999950000
assert sol.flowerGame(100000, 99999) == 4999950000
assert sol.flowerGame(1, 99999) == 49999
assert sol.flowerGame(99999, 1) == 49999
