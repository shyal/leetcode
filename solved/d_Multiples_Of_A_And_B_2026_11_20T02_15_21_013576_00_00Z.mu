# Given three positive integers n, a and b, return the number of integers x
# with 1 <= x <= n such that a divides x and b divides x.
#
# Example 1:
#
# Input: n = 12, a = 4, b = 6
# Output: 1
# Explanation: The integer is 12.
#
# Example 2:
#
# Input: n = 20, a = 2, b = 3
# Output: 3
# Explanation: The integers are 6, 12 and 18.
#
# Example 3:
#
# Input: n = 5, a = 2, b = 3
# Output: 0
#
# Use the least common multiple of a and b.
#
# Constraints:
#
#     1 <= n, a, b <= 10^12
#
#     REQUIRED: O(log(a + b)) time. NO loop over the integers from 1 to n.
#
# ---
# learning

# mu 0.18

class Solution
  def multiples(n: int, a: int, b: int) -> int
    c = a * b // gcd(a, b)
    n // c

sol = Solution()

print(sol.multiples(12, 4, 6))  # 1

assert sol.multiples(12, 4, 6) == 1
assert sol.multiples(20, 2, 3) == 3
assert sol.multiples(5, 2, 3) == 0
assert sol.multiples(11, 4, 6) == 0
assert sol.multiples(24, 4, 6) == 2
assert sol.multiples(9, 3, 3) == 3
assert sol.multiples(8, 1, 5) == 1
assert sol.multiples(20, 2, 4) == 5
assert sol.multiples(100, 6, 10) == 3
assert sol.multiples(1, 1, 1) == 1
assert sol.multiples(10 ** 12, 2, 3) == 166666666666
assert sol.multiples(10 ** 12, 10 ** 12, 10 ** 12) == 1
