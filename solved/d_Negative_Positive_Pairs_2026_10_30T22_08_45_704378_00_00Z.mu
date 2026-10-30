# Given two integer arrays a and b, return the number of index pairs (i, j)
# such that a[i] < 0 and b[j] > 0.
#
# Example 1:
#
# Input: a = [-2, 5, -1], b = [3, 0, 7, -4]
# Output: 4
# Explanation: -2 and -1 each pair with 3 and 7.
#
# Example 2:
#
# Input: a = [1, 2], b = [3]
# Output: 0
# Explanation: a has no negative value.
#
# Example 3:
#
# Input: a = [-1, -1], b = [0, 2]
# Output: 2
# Explanation: 0 is not positive. Each -1 pairs with 2.
#
# Constraints:
#
#     1 <= len(a), len(b) <= 10^5
#     -1000 <= a[i], b[j] <= 1000
#
#     REQUIRED: O(len(a) + len(b)). NO loop over pairs.
#
# ---

# mu 0.14

class Solution
  def negativePositivePairs(a: [int], b: [int]) -> int
    (count for a: _ < 0) * (count for b: _ > 0)

sol = Solution()

print(sol.negativePositivePairs([-2, 5, -1], [3, 0, 7, -4]))  # 4

assert sol.negativePositivePairs([-2, 5, -1], [3, 0, 7, -4]) == 4
assert sol.negativePositivePairs([1, 2], [3]) == 0
assert sol.negativePositivePairs([-1, -1], [0, 2]) == 2
assert sol.negativePositivePairs([-1], [1]) == 1
assert sol.negativePositivePairs([-1], [-1]) == 0
assert sol.negativePositivePairs([0], [0]) == 0
assert sol.negativePositivePairs([-3, 0, 3], [-3, 0, 3]) == 1
assert sol.negativePositivePairs([-1] * 100000, [1] * 100000) == 10000000000
assert sol.negativePositivePairs([-1] * 99999 + [1], [1] * 99999 + [-1]) == 9999800001
