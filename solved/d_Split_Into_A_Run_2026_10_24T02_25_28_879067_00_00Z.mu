# DRILL: Split Into A Run
# TRAINS: consecutive-sum-split
#
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
# Explanation: 3 + 4 + 5 + 6 = 18 and 2 + 3 + 4 + 5 = 14. No run of four
# positive integers sums to 15.
#
# Example 3:
#
# Input: n = 15, k = 6
# Output: False
# Explanation: The smallest run of six positive integers, 1 + 2 + 3 + 4 + 5 + 6,
# already sums to 21.
#
# Constraints:
#
#     1 <= n <= 10^9
#     1 <= k <= 10^5
#
#     REQUIRED: O(1), arithmetic on n and k only. NO loop. NO search for the
#     first integer of the run.
#
# ---
# learning

# mu 0.12

class Solution
  def sumOfRun(s: int, c: int) -> int
    prefix = s * (s - 1) // 2
    full = (s + c) * ((s + c) - 1) // 2
    full - prefix

  def splitIntoRun(n: int, k: int) -> bool
    rest = n - self.sumOfRun(1, k - 1)
    rest > 0 and rest % k == 0

sol = Solution()

print(sol.splitIntoRun(15, 3))  # True

assert sol.splitIntoRun(15, 3) is true
assert sol.splitIntoRun(15, 4) is false
assert sol.splitIntoRun(15, 6) is false
assert sol.splitIntoRun(15, 1) is true
assert sol.splitIntoRun(15, 2) is true
assert sol.splitIntoRun(15, 5) is true
assert sol.splitIntoRun(16, 2) is false
assert sol.splitIntoRun(16, 3) is false
assert sol.splitIntoRun(16, 4) is false
assert sol.splitIntoRun(16, 5) is false
assert sol.splitIntoRun(9, 2) is true
assert sol.splitIntoRun(9, 3) is true
assert sol.splitIntoRun(1, 1) is true
assert sol.splitIntoRun(1, 2) is false
assert sol.splitIntoRun(3, 2) is true
assert sol.splitIntoRun(10 ** 9, 44721) is false
assert sol.splitIntoRun(10 ** 9, 44720) is false
assert sol.splitIntoRun(10 ** 9, 25) is true
assert sol.splitIntoRun(10 ** 9, 10 ** 5) is false
