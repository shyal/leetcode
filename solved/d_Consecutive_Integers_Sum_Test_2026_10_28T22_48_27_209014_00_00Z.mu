# Given two positive integers n and k, return True if n is the sum of k
# consecutive positive integers, and False otherwise.
#
# Example 1:
#
# Input: n = 15, k = 3
# Output: True
# Explanation: 15 = 4 + 5 + 6.
#
# Example 2:
#
# Input: n = 15, k = 4
# Output: False
# Explanation: 3 + 4 + 5 + 6 = 18 and 2 + 3 + 4 + 5 = 14. No four consecutive
# positive integers sum to 15.
#
# Example 3:
#
# Input: n = 15, k = 6
# Output: False
# Explanation: The smallest six consecutive positive integers,
# 1 + 2 + 3 + 4 + 5 + 6, already sum to 21.
#
# Constraints:
#
#     1 <= n <= 10^9
#     1 <= k <= 10^5
#
#     REQUIRED: O(1), arithmetic on n and k only. NO loop. NO search for the
#     first integer of the sequence.
#
# ---

# mu 0.13

class Solution
  def isConsecutiveSum(n: int, k: int) -> bool
    rest = n - (k * (k - 1) // 2)
    rest > 0 and rest % k == 0

sol = Solution()

print(sol.isConsecutiveSum(15, 3))  # True

assert sol.isConsecutiveSum(15, 3) is true
assert sol.isConsecutiveSum(15, 4) is false
assert sol.isConsecutiveSum(15, 6) is false
assert sol.isConsecutiveSum(15, 1) is true
assert sol.isConsecutiveSum(15, 2) is true
assert sol.isConsecutiveSum(15, 5) is true
assert sol.isConsecutiveSum(16, 2) is false
assert sol.isConsecutiveSum(16, 3) is false
assert sol.isConsecutiveSum(16, 4) is false
assert sol.isConsecutiveSum(16, 5) is false
assert sol.isConsecutiveSum(9, 2) is true
assert sol.isConsecutiveSum(9, 3) is true
assert sol.isConsecutiveSum(1, 1) is true
assert sol.isConsecutiveSum(1, 2) is false
assert sol.isConsecutiveSum(3, 2) is true
assert sol.isConsecutiveSum(10 ** 9, 44721) is false
assert sol.isConsecutiveSum(10 ** 9, 44720) is false
assert sol.isConsecutiveSum(10 ** 9, 25) is true
assert sol.isConsecutiveSum(10 ** 9, 10 ** 5) is false
