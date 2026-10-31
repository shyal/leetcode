# URL: https://leetcode.com/problems/three-fibonacci-sum/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 4078. Three Fibonacci Sum
#
# You are given an integer n.
#
# The Fibonacci sequence starts with 0 and 1, and each subsequent number is the
# sum of the previous two numbers. Its first few terms are 0, 1, 1, 2, 3, 5, 8, 13, ...
#
# Return true if n can be expressed as the sum of three consecutive terms in the
# Fibonacci sequence, and false otherwise.
#
#
# Example 1:
#
# Input: n = 16
# Output: true
# Explanation: The three consecutive terms 3, 5, and 8 have a sum of 3 + 5 + 8 = 16.
#
# Example 2:
#
# Input: n = 8
# Output: false
# Explanation: Although 1 + 2 + 5 = 8, these terms are not consecutive in the
# Fibonacci sequence. No three consecutive terms have a sum of 8.
#
# Example 3:
#
# Input: n = 2
# Output: true
# Explanation: The first three terms have a sum of 0 + 1 + 1 = 2.
#
#
# Constraints:
#
#     1 <= n <= 10^9
#
# ---
# LEETCODE: Accepted (0 ms, 19.1 MB)

# mu 0.14

class Solution
  def threeFibonacciSum(n: int) -> bool
    p, pp, ppp = 0, 1..
    for i in 2..n
      res = p + pp
      ppp = pp
      pp = p
      p = res
      if p + pp + ppp == n
        return true
      if res > n
        break
    false

sol = Solution()

print(sol.threeFibonacciSum(16))  # True

assert sol.threeFibonacciSum(16) is true
assert sol.threeFibonacciSum(8) is false
assert sol.threeFibonacciSum(2) is true
assert sol.threeFibonacciSum(1) == false
assert sol.threeFibonacciSum(3) == false
assert sol.threeFibonacciSum(4) == true
assert sol.threeFibonacciSum(6) == true
assert sol.threeFibonacciSum(10) == true
assert sol.threeFibonacciSum(12) == false
assert sol.threeFibonacciSum(26) == true
assert sol.threeFibonacciSum(535828592) == true
assert sol.threeFibonacciSum(535828590) == false
assert sol.threeFibonacciSum(866988874) == true
assert sol.threeFibonacciSum(866988875) == false
assert sol.threeFibonacciSum(1000000000) == false

# edge cases: one line each, the values are the reference solution's.
assert Solution().threeFibonacciSum(1) == false  # smallest_n_allowed
assert Solution().threeFibonacciSum(2) == true  # first_three_terms_zero_one_one
assert Solution().threeFibonacciSum(3) == false  # n_is_a_fibonacci_term_and_odd
assert Solution().threeFibonacciSum(5) == false  # n_is_a_fibonacci_term_but_not_a_three_term_sum
assert Solution().threeFibonacciSum(8) == false  # n_is_sum_of_three_nonconsecutive_terms
assert Solution().threeFibonacciSum(13) == false  # n_is_fibonacci_term_between_two_valid_sums
assert Solution().threeFibonacciSum(14) == false  # even_n_just_below_a_valid_sum
assert Solution().threeFibonacciSum(20) == false  # even_n_twice_a_non_fibonacci_number
assert Solution().threeFibonacciSum(42) == true  # sum_of_8_13_21
assert Solution().threeFibonacciSum(866988874) == true  # largest_valid_sum_within_constraints
assert Solution().threeFibonacciSum(866988873) == false  # one_below_largest_valid_sum
assert Solution().threeFibonacciSum(1000000000) == false  # maximum_n_allowed
