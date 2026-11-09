# Given integers a, b and m with 0 <= a, b < m, return the smallest
# integer k >= 0 such that (a + k) mod m == b or (a - k) mod m == b.
#
# For example, a = 1, b = 9, m = 10. k = 8 works: (1 + 8) mod 10 == 9.
# k = 2 also works: (1 - 2) mod 10 == -1 mod 10 == 9. No smaller k works.
# Return 2.
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
# Explanation: (0 + 5) mod 10 == 5 and (0 - 5) mod 10 == 5. Both need k = 5.
#
# Constraints:
#
#     2 <= m <= 10^9
#     0 <= a, b < m
#
#     REQUIRED: O(1), arithmetic only. NO loop over k.
#
# ---
# learning

# mu 0.16

class Solution
  def dist(a: int, b: int, m: int) -> int
    d = abs(a - b)
    min(d, m - d)

sol = Solution()

print(sol.dist(1, 9, 10))  # 2

# assert sol.dist(1, 9, 10) == 2
# assert sol.dist(3, 7, 10) == 4
# assert sol.dist(0, 5, 10) == 5
# assert sol.dist(9, 1, 10) == 2
# assert sol.dist(4, 4, 10) == 0
# assert sol.dist(0, 9, 10) == 1
# assert sol.dist(9, 0, 10) == 1
# assert sol.dist(0, 1, 2) == 1
# assert sol.dist(0, 10 ** 9 - 1, 10 ** 9) == 1
# assert sol.dist(0, 10 ** 9 // 2, 10 ** 9) == 10 ** 9 // 2
# assert sol.dist(2, 11, 12) == 3
