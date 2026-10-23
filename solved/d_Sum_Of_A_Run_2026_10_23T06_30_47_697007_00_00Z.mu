# DRILL: Sum Of A Run
# TRAINS: consecutive-sum-split
#
# Given two positive integers n and k, return the sum of the k consecutive
# integers that start at n: n + (n + 1) + ... + (n + k - 1).
#
# Example 1:
#
# Input: n = 4, k = 3
# Output: 15
# Explanation: 4 + 5 + 6 = 15.
#
# Example 2:
#
# Input: n = 1, k = 100
# Output: 5050
#
# Example 3:
#
# Input: n = 7, k = 1
# Output: 7
# Explanation: A run of one integer is the integer itself.
#
# Constraints:
#
#     1 <= n <= 10^9
#     1 <= k <= 10^5
#
#     REQUIRED: O(1), one arithmetic expression. NO loop. NO sum. NO range.
#
# ---
# Learning

# mu 0.12

class Solution
  def sumOfRun(n: int, k: int) -> int
    k * (2 * n + k - 1) // 2

sol = Solution()

print(sol.sumOfRun(4, 3))  # 15

assert sol.sumOfRun(4, 3) == 15
assert sol.sumOfRun(1, 100) == 5050
assert sol.sumOfRun(7, 1) == 7
assert sol.sumOfRun(7, 2) == 15
assert sol.sumOfRun(1, 5) == 15
assert sol.sumOfRun(8, 2) == 17
assert sol.sumOfRun(100, 3) == 303
assert sol.sumOfRun(10 ** 9, 10 ** 5) == sum(10 ** 9..<10 ** 9 + 10 ** 5)
assert sol.sumOfRun(1, 1) == 1
