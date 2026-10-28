# Given an integer array nums, return the number of subarrays in which
# every element is even. A subarray is a contiguous non-empty part of
# nums. Two subarrays with the same values at different positions are two
# subarrays.
#
# Example 1:
#
# Input: nums = [2, 4, 1, 6, 8, 10, 3]
# Output: 9
# Explanation: [2, 4] holds [2], [4], [2, 4]. [6, 8, 10] holds [6], [8],
# [10], [6, 8], [8, 10], [6, 8, 10]. Nothing else is all even.
#
# Example 2:
#
# Input: nums = [1, 3, 5]
# Output: 0
#
# Example 3:
#
# Input: nums = [2, 2, 2]
# Output: 6
#
# Constraints:
#
#     1 <= len(nums) <= 10^5
#     0 <= nums[i] <= 10^9
#
#     REQUIRED: O(n). NO loop over the start and end of every subarray.
#
# Use count_subarrays.
#
# ---

# mu 0.13

class Solution
  def evenSubarrays(nums: [int]) -> int
    count_subarrays(nums, key= x -> even(x))

sol = Solution()

print(sol.evenSubarrays([2, 4, 1, 6, 8, 10, 3]))  # 9

assert sol.evenSubarrays([2, 4, 1, 6, 8, 10, 3]) == 9
assert sol.evenSubarrays([1, 3, 5]) == 0
assert sol.evenSubarrays([2, 2, 2]) == 6
assert sol.evenSubarrays([2]) == 1
assert sol.evenSubarrays([1]) == 0
assert sol.evenSubarrays([1, 2]) == 1
assert sol.evenSubarrays([2, 1]) == 1
assert sol.evenSubarrays([0] * 100000) == 100000 * 100001 // 2
