# URL: https://leetcode.com/problems/minimum-positive-sum-subarray/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 3364. Minimum Positive Sum Subarray
#
# You are given an integer array nums and two integers l and r. Your task is to find the minimum sum of a subarray whose size is between l and r (inclusive) and whose sum is greater than 0.
#
# Return the minimum sum of such a subarray. If no such subarray exists, return -1.
#
# A subarray is a contiguous non-empty sequence of elements within an array.
#
# Example 1:
#
# Input: nums = [3, -2, 1, 4], l = 2, r = 3
# Output: 1
# Explanation:
# The subarrays of length between l = 2 and r = 3 where the sum is greater than 0 are:
# - [3, -2] with a sum of 1
# - [1, 4] with a sum of 5
# - [3, -2, 1] with a sum of 2
# - [-2, 1, 4] with a sum of 3
# Out of these, the subarray [3, -2] has a sum of 1, which is the smallest positive sum. Hence, the answer is 1.
#
# Example 2:
#
# Input: nums = [-2, 2, -3, 1], l = 2, r = 3
# Output: -1
# Explanation:
# There is no subarray of length between l and r that has a sum greater than 0. So, the answer is -1.
#
# Example 3:
#
# Input: nums = [1, 2, 3, 4], l = 2, r = 4
# Output: 3
# Explanation:
# The subarray [1, 2] has a length of 2 and the minimum sum greater than 0. So, the answer is 3.
#
# Constraints:
#
#     1 <= nums.length <= 100
#     1 <= l <= r <= nums.length
#     -1000 <= nums[i] <= 1000
#
# ---
# STAGE 1 of 3 - the approach. Write it in plain English under this line. Then run make solved.
# LEETCODE: Accepted (46 ms, 19.2 MB)

# mu 0.18

class Solution
  def rangeSum(i, j)
    self.p[j] - (self.p[i - 1] if i > 0 else 0)

  def minimumSumSubarray(nums: [int], l: int, r: int) -> int
    self.p = [*scan(+, nums)]
    best = inf
    for >i in nums
      for j in i..<len(nums)
        if l <= j - i + 1 <= r
          sum = self.rangeSum(i, j)
          if sum > 0
            best = min(sum, best)
    if best != inf
      return best
    -1

sol = Solution()

print(sol.minimumSumSubarray([3, -2, 1, 4], 2, 3))  # 1
assert sol.minimumSumSubarray([3, -2, 1, 4], 2, 3) == 1
assert sol.minimumSumSubarray([-2, 2, -3, 1], 2, 3) == -1
assert sol.minimumSumSubarray([1, 2, 3, 4], 2, 4) == 3
assert sol.minimumSumSubarray([1], 1, 1) == 1
assert sol.minimumSumSubarray([-1], 1, 1) == -1
assert sol.minimumSumSubarray([0, 0, 0], 1, 3) == -1
assert sol.minimumSumSubarray([1000] * 100, 1, 100) == 1000
assert sol.minimumSumSubarray([-1000] * 100, 1, 100) == -1
assert sol.minimumSumSubarray([1, -1, 1, -1, 1, -1], 1, 2) == 1
assert sol.minimumSumSubarray([5, 5, 5, 5], 2, 2) == 10
assert sol.minimumSumSubarray([1, 2, 3, -10, 5, 6], 3, 5) == 1
assert sol.minimumSumSubarray([1, 1, 1, 1, 1], 1, 5) == 1
assert sol.minimumSumSubarray([10, -5, 10, -5, 10], 2, 3) == 5
assert sol.minimumSumSubarray([-1, -2, -3, -4, -5], 1, 5) == -1
assert sol.minimumSumSubarray([0, 1, 0, 1, 0], 1, 3) == 1
