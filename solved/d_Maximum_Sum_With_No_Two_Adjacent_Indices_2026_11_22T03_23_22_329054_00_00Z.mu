# Given an integer array nums of length n, choose indices of nums and
# return the maximum sum of nums over the chosen indices. You must not
# choose two adjacent indices i and i + 1.
#
# Example 1:
#
# Input: nums = [2, 7, 9, 3, 1]
# Output: 12
# Explanation: indices 0, 2 and 4: 2 + 9 + 1.
#
# Example 2:
#
# Input: nums = [2, 1, 1, 2]
# Output: 4
# Explanation: indices 0 and 3: 2 + 2.
#
# Example 3:
#
# Input: nums = [5]
# Output: 5
#
# Constraints:
#
#     1 <= n <= 10^5
#     0 <= nums[i] <= 10^4
#
#     REQUIRED: O(n) time.
#
# ---

# mu 0.20

class Solution
  def maxSum(nums: [int]) -> int
    max(
    memo {
      i -> i >= len nums: 0, 0
        max(s, t), nums[i] + s = mu(i + 1)
    }(0))

sol = Solution()

print(sol.maxSum([2, 7, 9, 3, 1]))  # 12

assert sol.maxSum([2, 7, 9, 3, 1]) == 12
assert sol.maxSum([2, 1, 1, 2]) == 4
assert sol.maxSum([5]) == 5
assert sol.maxSum([1, 2, 3, 1]) == 4
assert sol.maxSum([0, 0, 0]) == 0
assert sol.maxSum([5, 1]) == 5
assert sol.maxSum([1, 5]) == 5
assert sol.maxSum([4, 4, 4, 4]) == 8
assert sol.maxSum([1, 9, 10, 9]) == 18
assert sol.maxSum([10, 1, 1, 10, 1]) == 20
assert sol.maxSum([1, 2, 3, 4, 5, 6]) == 12
assert sol.maxSum([6, 5, 4, 3, 2, 1]) == 12
assert sol.maxSum([3, 10, 3, 1, 2, 10, 3]) == 21
assert sol.maxSum([10000] * 100000) == 500000000
assert sol.maxSum([1, 0] * 50000) == 50000
