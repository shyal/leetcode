# Given an integer array nums, return the largest alternating sum of a
# non-empty subarray. The alternating sum of a subarray is its first
# element minus its second plus its third, and so on: the elements at even
# positions in the subarray are added, the elements at odd positions are
# subtracted.
#
# Example 1:
#
# Input: nums = [-54, 77, 97]
# Output: 97
# Explanation: the subarray [97]; the whole array gives -54 - 77 + 97 = -34.
#
# Example 2:
#
# Input: nums = [10, -100]
# Output: 110
# Explanation: the whole array, 10 - (-100); the answer ends on a
# subtracted element.
#
# Example 3:
#
# Input: nums = [3, 8, 1, 9]
# Output: 16
# Explanation: the subarray [8, 1, 9], 8 - 1 + 9.
#
# Constraints:
#
#     1 <= len(nums) <= 10^5
#     -10^5 <= nums[i] <= 10^5
#
#     REQUIRED: O(n) time, O(1) extra space, a single pass. NO enumeration
#     of subarrays. The empty subarray is not allowed.
#
# ---
# learning

class Solution
  def maxAlternatingSum(nums: [int]) -> int
    n = len nums
    memo best(i, s) =
     | i == n         ->    -inf
     | else           ->    nums[i] * s + max(0, best(i + 1, -s))
    max for x in 0..n: best(x, 1)

sol = Solution()

print(sol.maxAlternatingSum([-54, 77, 97]))  # 97

assert sol.maxAlternatingSum([-54, 77, 97]) == 97
assert sol.maxAlternatingSum([10, -100]) == 110
assert sol.maxAlternatingSum([3, 8, 1, 9]) == 16
assert sol.maxAlternatingSum([5, -5, 1]) == 11
assert sol.maxAlternatingSum([4, 7]) == 7
assert sol.maxAlternatingSum([-72]) == -72
assert sol.maxAlternatingSum([-5, -5]) == 0
assert sol.maxAlternatingSum([1, -1, 1, -1, 1]) == 5
assert sol.maxAlternatingSum([9, 1, 1, 1, 1, 1, 1, 1]) == 9
assert sol.maxAlternatingSum([1, 1, 1, 1, 1, 1, 1, 9]) == 9
assert sol.maxAlternatingSum([1, 1, 1, 9, 1, 1, 1, 1]) == 9
assert sol.maxAlternatingSum([2, -3, 2, -3, 2, -3, 2, -3]) == 20
assert sol.maxAlternatingSum([1, -1] * 50000) == 100000
assert sol.maxAlternatingSum([10 ** 5] * 10 ** 5) == 10 ** 5
assert sol.maxAlternatingSum([-10 ** 5] * 10 ** 5) == 0
