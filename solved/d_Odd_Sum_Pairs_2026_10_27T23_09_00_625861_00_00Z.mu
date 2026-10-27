# Given two integer arrays a and b, return the number of index pairs (i, j)
# such that a[i] + b[j] is odd.
#
# Example 1:
#
# Input: a = [1, 2, 3], b = [4, 5]
# Output: 3
# Explanation: the pairs are (1, 4), (3, 4) and (2, 5).
#
# Example 2:
#
# Input: a = [2, 4], b = [6]
# Output: 0
# Explanation: every sum is even.
#
# Example 3:
#
# Input: a = [0, -3], b = [7]
# Output: 1
# Explanation: 0 + 7 is odd. -3 + 7 is even.
#
# Constraints:
#
#     1 <= len(a), len(b) <= 10^5
#     -1000 <= a[i], b[j] <= 1000
#
#     REQUIRED: O(len(a) + len(b)). NO loop over pairs. NO sum x + y
#     computed.
#
# ---

# mu 0.13

class Solution
  def oddSumPairs(a: [int], b: [int]) -> int
    (count for a: odd(_)) * (count for b: even(_)) + (count for a: even(_)) * (count for b: odd(_))

sol = Solution()

print(sol.oddSumPairs([1, 2, 3], [4, 5]))  # 3

assert sol.oddSumPairs([1, 2, 3], [4, 5]) == 3
assert sol.oddSumPairs([2, 4], [6]) == 0
assert sol.oddSumPairs([0, -3], [7]) == 1
assert sol.oddSumPairs([1], [1]) == 0
assert sol.oddSumPairs([1], [2]) == 1
assert sol.oddSumPairs([1, 1], [2, 2]) == 4
assert sol.oddSumPairs([1, 2, 3, 4], [1, 2, 3, 4]) == 8
assert sol.oddSumPairs([-1, -2], [-3, -4]) == 2
assert sol.oddSumPairs([1] * 100000, [2] * 100000) == 10000000000
assert sol.oddSumPairs([1] * 100000, [1] * 100000) == 0
assert sol.oddSumPairs([1, 2] * 50000, [1, 2] * 50000) == 5000000000
