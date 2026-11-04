# URL: https://leetcode.com/problems/number-of-subarrays-with-gcd-equal-to-k/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 2447. Number of Subarrays With GCD Equal to K
#
# Given an integer array nums and an integer k, return the number of subarrays of nums where the greatest common divisor of the subarray's elements is k.
#
# A subarray is a contiguous non-empty sequence of elements within an array.
#
# The greatest common divisor of an array is the largest integer that evenly divides all the array elements.
#
# Example 1:
#
# Input: nums = [9,3,1,2,6,3], k = 3
# Output: 4
# Explanation: The subarrays of nums where 3 is the greatest common divisor of all the subarray's elements are:
# - [9,3]
# - [3]
# - [6,3]
# - [3]
#
# Example 2:
#
# Input: nums = [4], k = 7
# Output: 0
# Explanation: There are no subarrays of nums where 7 is the greatest common divisor of all the subarray's elements.
#
# Constraints:
#
#     1 <= nums.length <= 1000
#     1 <= nums[i], k <= 10^9
#
# ---
# Learning

class Solution
  def subarrayGCD(nums: [int], k: int) -> int
    ret count = 0
    for >i in nums
      g = 0
      for x in nums[i:]
        g = gcd(g, x)
        count += g == k

sol = Solution()

print(sol.subarrayGCD([9, 3, 1, 2, 6, 3], 3))  # 4

assert sol.subarrayGCD([9, 3, 1, 2, 6, 3], 3) == 4
assert sol.subarrayGCD([4], 7) == 0
assert sol.subarrayGCD([1], 1) == 1
assert sol.subarrayGCD([2, 4, 6, 8, 10], 2) == 11
assert sol.subarrayGCD([5, 5, 5, 5], 5) == 10
assert sol.subarrayGCD([10 ** 9, 10 ** 9, 10 ** 9], 10 ** 9) == 6
assert sol.subarrayGCD([3, 6, 9, 12, 15], 3) == 11
assert sol.subarrayGCD([7, 14, 21, 28], 7) == 7
assert sol.subarrayGCD([2, 3, 5, 7, 11, 13], 1) == 15
assert sol.subarrayGCD([12, 15, 18, 21, 24], 3) == 10
assert sol.subarrayGCD([1000] * 1000, 1000) == 500500
assert sol.subarrayGCD([6, 9, 12, 15, 18], 6) == 1
assert sol.subarrayGCD([1, 1, 1, 1, 1], 1) == 15
assert sol.subarrayGCD([17], 17) == 1
