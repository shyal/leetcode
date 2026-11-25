# Given an array nums of positive integers and an integer target, return
# true if a subset of nums has a sum equal to target, or false otherwise.
#
# Example 1:
#
# Input: nums = [1, 5, 11, 5], target = 11
# Output: true
# Explanation: The subset [1, 5, 5] has the sum 11.
#
# Example 2:
#
# Input: nums = [2, 4, 8], target = 5
# Output: false
#
# Example 3:
#
# Input: nums = [3, 3], target = 9
# Output: false
# Explanation: A subset uses each element of nums at most once.
#
# Constraints:
#
#     1 <= nums.length <= 200
#     1 <= nums[i] <= 100
#     1 <= target <= 10^4
#
#     REQUIRED: O(nums.length * target) time.
#
# ---

# mu 0.20

class Solution
  def subsetSum(nums: [int], target: int) -> bool
    sums = set([0])
    for x in nums
      sums |= {x + s for s in sums if x + s <= target}
    target in sums

sol = Solution()

print(sol.subsetSum([1, 5, 10, 5], 11))  # True

assert sol.subsetSum([1, 5, 11, 5], 11) == true
assert sol.subsetSum([2, 4, 8], 5) == false
assert sol.subsetSum([3, 3], 9) == false
assert sol.subsetSum([3, 3], 6) == true
assert sol.subsetSum([3, 3], 3) == true
assert sol.subsetSum([7], 7) == true
assert sol.subsetSum([7], 6) == false
assert sol.subsetSum([1, 2, 3, 5], 11) == true
assert sol.subsetSum([1, 2, 3, 5], 7) == true
assert sol.subsetSum([1, 2, 3, 5], 12) == false
assert sol.subsetSum([2, 2, 2, 2], 5) == false
assert sol.subsetSum([2, 2, 2, 2], 8) == true
assert sol.subsetSum([5, 1, 1], 2) == true
assert sol.subsetSum([5, 1, 1], 3) == false
assert sol.subsetSum([10, 20, 30, 40, 50], 90) == true
assert sol.subsetSum([10, 20, 30, 40, 50], 95) == false
assert sol.subsetSum([100] * 200, 9999) == false
assert sol.subsetSum([100] * 200, 10000) == true
assert sol.subsetSum(list(1..<101) * 2, 10000) == true
