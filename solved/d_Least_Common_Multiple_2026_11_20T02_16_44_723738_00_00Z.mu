# Given two positive integers a and b, return the smallest positive integer
# that a and b both divide.
#
# Example 1:
#
# Input: a = 4, b = 6
# Output: 12
# Explanation: 4 divides 12, 6 divides 12, and no smaller positive integer
# has both divisors.
#
# Example 2:
#
# Input: a = 2, b = 3
# Output: 6
#
# Example 3:
#
# Input: a = 2, b = 4
# Output: 4
#
# Constraints:
#
#     1 <= a, b <= 10^12
#
#     REQUIRED: O(log(a + b)) time. NO lcm(). NO loop over the multiples of a.
#
# ---

# mu 0.18

class Solution
  def lcm(a: int, b: int) -> int
    a * b // gcd(a, b)

sol = Solution()

print(sol.lcm(4, 6))  # 12

assert sol.lcm(4, 6) == 12
assert sol.lcm(2, 3) == 6
assert sol.lcm(2, 4) == 4
assert sol.lcm(4, 2) == 4
assert sol.lcm(3, 3) == 3
assert sol.lcm(1, 5) == 5
assert sol.lcm(1, 1) == 1
assert sol.lcm(6, 10) == 30
assert sol.lcm(12, 18) == 36
assert sol.lcm(10 ** 12, 2) == 10 ** 12
assert sol.lcm(10 ** 12, 10 ** 12) == 10 ** 12
assert sol.lcm(10 ** 12, 10 ** 12 - 1) == 10 ** 12 * (10 ** 12 - 1)
