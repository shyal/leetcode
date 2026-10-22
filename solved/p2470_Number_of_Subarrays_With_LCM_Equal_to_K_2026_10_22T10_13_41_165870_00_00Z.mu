# URL: https://leetcode.com/problems/number-of-subarrays-with-lcm-equal-to-k/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 2470. Number of Subarrays With LCM Equal to K
#
# Given an integer array nums and an integer k, return the number of subarrays of nums where the least common multiple of the subarray's elements is k.
#
# A subarray is a contiguous non-empty sequence of elements within an array.
#
# The least common multiple of an array is the smallest positive integer that is divisible by all the array elements.
#
# Example 1:
#
# Input: nums = [3,6,2,7,1], k = 6
# Output: 4
# Explanation: The subarrays of nums where 6 is the least common multiple of all the subarray's elements are:
# - [3,6,2,7,1]
# - [3,6,2,7,1]
# - [3,6,2,7,1]
# - [3,6,2,7,1]
#
# Example 2:
#
# Input: nums = [3], k = 2
# Output: 0
# Explanation: There are no subarrays of nums where 2 is the least common multiple of all the subarray's elements.
#
# Constraints:
#
#     1 <= nums.length <= 1000
#     1 <= nums[i], k <= 1000
#
# ---
# LEETCODE: Accepted (245 ms, 19.3 MB)

# mu 0.12

class Solution
  def subarrayLCM(nums: [int], k: int) -> int
    def lcm(a, b)
      return int(a * b / gcd(a, b))
    
    ret res = 0
    for i in 0..<len(nums)
      l = 1
      for j in i..<len(nums)
        l = lcm(l, nums[j])
        res += l == k
        if l > k
          break
        # print(l, end=', ')
      # print(l)
        


sol = Solution()

print(sol.subarrayLCM([3, 6, 2, 7, 1], 6))  # 4

assert sol.subarrayLCM([3, 6, 2, 7, 1], 6) == 4
assert sol.subarrayLCM([3], 2) == 0
assert sol.subarrayLCM([1], 1) == 1
assert sol.subarrayLCM([1000], 1000) == 1
assert sol.subarrayLCM([2, 2, 2, 2], 2) == 10
assert sol.subarrayLCM([2, 3, 5, 7], 210) == 1
assert sol.subarrayLCM([2, 3, 5, 7], 30) == 1
assert sol.subarrayLCM([1, 1, 1, 1, 1], 1) == 15
assert sol.subarrayLCM([10, 5, 2, 1], 10) == 6
assert sol.subarrayLCM([4, 6, 8, 12], 24) == 5
assert sol.subarrayLCM([1] * 1000, 1) == 500500
assert sol.subarrayLCM([1000] * 1000, 1000) == 500500
assert sol.subarrayLCM([2] * 500 + [3] * 500, 6) == 250000
assert sol.subarrayLCM([999, 1000, 1, 2], 1000) == 3
