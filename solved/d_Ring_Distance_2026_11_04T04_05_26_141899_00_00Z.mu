# A ring has m positions, numbered 0 to m - 1, like the numbers on a
# clock face. Position m - 1 is adjacent to position 0. One step moves
# from a position to one of its two adjacent positions.
#
# Given two positions a and b on the ring, return the smallest number of
# steps from a to b.
#
# A ring with m = 10:
#
#           0
#       9       1
#     8           2
#     7           3
#       6       4
#           5
#
# There are two routes from a to b. One route does not pass between 9 and
# 0. Its length is abs(a - b). The other route does pass between 9 and 0.
# Its length is m - abs(a - b). Return the shorter of the two.
#
# For example, a = 1, b = 9, m = 10. The route that does not pass between
# 9 and 0 is 1, 2, 3, 4, 5, 6, 7, 8, 9: 8 steps. The route that passes
# between 9 and 0 is 1, 0, 9: 2 steps. Return 2.
#
# Example 1:
#
# Input: a = 1, b = 9, m = 10
# Output: 2
#
# Example 2:
#
# Input: a = 3, b = 7, m = 10
# Output: 4
#
# Example 3:
#
# Input: a = 0, b = 5, m = 10
# Output: 5
# Explanation: both routes take 5 steps.
#
# Constraints:
#
#     2 <= m <= 10^9
#     0 <= a, b < m
#
#     REQUIRED: O(1), arithmetic only. No loop. abs(a - b) alone is wrong:
#     it returns 8 on Example 1.
#
# ---

# mu 0.16

class Solution
  def dist(a: int, b: int, m: int) -> int
    d = abs(a - b)
    min(d, m - d)

sol = Solution()

print(sol.dist(1, 9, 10))  # 2

assert sol.dist(1, 9, 10) == 2
assert sol.dist(3, 7, 10) == 4
assert sol.dist(0, 5, 10) == 5
assert sol.dist(9, 1, 10) == 2
assert sol.dist(4, 4, 10) == 0
assert sol.dist(0, 9, 10) == 1
assert sol.dist(9, 0, 10) == 1
assert sol.dist(0, 1, 2) == 1
assert sol.dist(0, 10 ** 9 - 1, 10 ** 9) == 1
assert sol.dist(0, 10 ** 9 // 2, 10 ** 9) == 10 ** 9 // 2
assert sol.dist(2, 11, 12) == 3
