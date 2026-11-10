# Given an integer array nums, return the largest alternating sum of a
# non-empty subarray. The alternating sum of a subarray is its first
# element minus its second plus its third, and so on: the elements at even
# positions in the subarray are added, the elements at odd positions are
# subtracted.
#
# Example 1:
#
# Input: nums = [1, 2, 3]
# Output: 3
# Explanation: the subarray [3]; the whole array gives 1 - 2 + 3 = 2.
#
# Example 2:
#
# Input: nums = [1, -5]
# Output: 6
# Explanation: the whole array, 1 - (-5); the answer ends on a subtracted
# element.
#
# Example 3:
#
# Input: nums = [2, 5, 1, 4]
# Output: 8
# Explanation: the subarray [5, 1, 4], 5 - 1 + 4.
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

# mu 0.17

class Solution
  def maxAlternatingSum(nums: [int]) -> int
    n = len nums
    memo best(s, i) =
      | i == n    ->    -inf
      |           ->    nums[i] * s + max(0, best(-s, i+1))
    max for >i in nums: best(1, i)

sol = Solution()

print(sol.maxAlternatingSum([1, 2, 3]))  # 3

assert sol.maxAlternatingSum([1, 2, 3]) == 3
assert sol.maxAlternatingSum([1, -5]) == 6
assert sol.maxAlternatingSum([2, 5, 1, 4]) == 8
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
