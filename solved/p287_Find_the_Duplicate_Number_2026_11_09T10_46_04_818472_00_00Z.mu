# URL: https://leetcode.com/problems/find-the-duplicate-number/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 287. Find the Duplicate Number
#
# Given an array of integers nums containing n + 1 integers where each integer is in the range [1, n] inclusive.
#
# There is only one repeated number in nums, return this repeated number.
#
# You must solve the problem without modifying the array nums and using only constant extra space.
#
# Example 1:
#
# Input: nums = [1,3,4,2,2]
# Output: 2
#
# Example 2:
#
# Input: nums = [3,1,3,4,2]
# Output: 3
#
# Example 3:
#
# Input: nums = [3,3,3,3,3]
# Output: 3
#
# Constraints:
#
#     1 <= n <= 10^5
#     nums.length == n + 1
#     1 <= nums[i] <= n
#     All the integers in nums appear only once except for precisely one integer which appears two or more times.
#
# Follow up:
#
#     How can we prove that at least one duplicate number must exist in nums?
#     Can you solve the problem in linear runtime complexity?
#
# ---
# LEETCODE: Accepted (36 ms, 33.3 MB)

# mu 0.16

class Solution
  def findDuplicate(nums: [int]) -> int
    slow_i, fast_i = 0
    while true
      slow_i, fast_i = nums[slow_i], nums[nums[fast_i]]
      if nums[slow_i] == nums[fast_i]
        b = slow_i
        break
    a = 0
    while nums[a] != nums[b]
      a = nums[a]
      b = nums[b]
    return nums[a]
    

sol = Solution()

print(sol.findDuplicate([2,5,9,6,9,3,8,9,7,1]))  # 2

assert sol.findDuplicate([1, 3, 4, 2, 2]) == 2
assert sol.findDuplicate([3, 1, 3, 4, 2]) == 3
assert sol.findDuplicate([3, 3, 3, 3, 3]) == 3
assert sol.findDuplicate([1, 1]) == 1
assert sol.findDuplicate([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10]) == 10
assert sol.findDuplicate([2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]) == 2
assert sol.findDuplicate([1, 2, 3, 4, 5, 6, 7, 8, 9, 1]) == 1
assert sol.findDuplicate([5, 1, 2, 3, 4, 5]) == 5
assert sol.findDuplicate([i for i in 1..<10 ** 5] + [10 ** 5 - 1]) == 99999
assert sol.findDuplicate([1, 2, 3, 4, 5, 6, 7, 8, 9, 9]) == 9
assert sol.findDuplicate([3, 1, 4, 2, 5, 6, 7, 8, 9, 10, 3]) == 3
assert sol.findDuplicate([1, 1, 2]) == 1
assert sol.findDuplicate([2, 1, 2]) == 2
assert sol.findDuplicate([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1]) == 1
assert sol.findDuplicate([2, 5, 9, 6, 9, 3, 8, 9, 7, 1]) == 9
