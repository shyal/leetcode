# URL: https://leetcode.com/problems/k-radius-subarray-averages/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 2090. K Radius Subarray Averages
#
# You are given a 0-indexed array nums of n integers, and an integer k.
#
# The k-radius average for a subarray of nums centered at some index i with the radius k is the average of all elements in nums between the indices i - k and i + k (inclusive). If there are less than k elements before or after the index i, then the k-radius average is -1.
#
# Build and return an array avgs of length n where avgs[i] is the k-radius average for the subarray centered at index i.
#
# The average of x elements is the sum of the x elements divided by x, using integer division. The integer division truncates toward zero, which means losing its fractional part.
#
# For example, the average of four elements 2, 3, 1, and 5 is (2 + 3 + 1 + 5) / 4 = 11 / 4 = 2.75, which truncates to 2.
#
# Example 1:
#
# Input: nums = [7,4,3,9,1,8,5,2,6], k = 3
# Output: [-1,-1,-1,5,4,4,-1,-1,-1]
# Explanation:
# - avg[0], avg[1], and avg[2] are -1 because there are less than k elements before each index.
# - The sum of the subarray centered at index 3 with radius 3 is: 7 + 4 + 3 + 9 + 1 + 8 + 5 = 37.
#   Using integer division, avg[3] = 37 / 7 = 5.
# - For the subarray centered at index 4, avg[4] = (4 + 3 + 9 + 1 + 8 + 5 + 2) / 7 = 4.
# - For the subarray centered at index 5, avg[5] = (3 + 9 + 1 + 8 + 5 + 2 + 6) / 7 = 4.
# - avg[6], avg[7], and avg[8] are -1 because there are less than k elements after each index.
#
# Example 2:
#
# Input: nums = [100000], k = 0
# Output: [100000]
# Explanation:
# - The sum of the subarray centered at index 0 with radius 0 is: 100000.
#   avg[0] = 100000 / 1 = 100000.
#
# Example 3:
#
# Input: nums = [8], k = 100000
# Output: [-1]
# Explanation:
# - avg[0] is -1 because there are less than k elements before and after index 0.
#
# Constraints:
#
#     n == nums.length
#     1 <= n <= 10^5
#     0 <= nums[i], k <= 10^5
#
# ---
# STAGE 1 of 3 - the approach. Write it in plain English under this line. Then run make solved.
#
# LEETCODE: Accepted (173 ms, 37.9 MB)

# mu 0.18

class Solution
  def get_range(i, j)
    self.p[j] - (i > 0 ? self.p[i - 1] : 0)
  def getAverages(nums: [int], k: int) -> [int]
    self.nums = nums
    self.p = [*scan(+, nums)]
    ret res = []
    for >i in nums
      if i >= k and i + k <= len(nums) - 1
        res <- floor(self.get_range(i -k, i + k) / (2k + 1))
      else
        res <- -1

sol = Solution()

print(sol.getAverages([7, 4, 3, 9, 1, 8, 5, 2, 6], 3))  # [-1,-1,-1,5,4,4,-1,-1,-1]

assert sol.getAverages([7, 4, 3, 9, 1, 8, 5, 2, 6], 3) == [-1, -1, -1, 5, 4, 4, -1, -1, -1]
assert sol.getAverages([100000], 0) == [100000]
assert sol.getAverages([8], 100000) == [-1]
assert sol.getAverages([], 0) == []
assert sol.getAverages([1], 0) == [1]
assert sol.getAverages([1], 1) == [-1]
assert sol.getAverages([1, 1, 1, 1, 1], 2) == [-1, -1, 1, -1, -1]
assert sol.getAverages([1, 2, 3, 4, 5], 0) == [1, 2, 3, 4, 5]
assert sol.getAverages([5, 5, 5, 5, 5], 1) == [-1, 5, 5, 5, -1]
assert sol.getAverages([1, -1, 1, -1, 1, -1, 1, -1], 1) == [-1, 0, -1, 0, -1, 0, -1, -1]
assert sol.getAverages([1] * 3 + [10 ** 5] * 3 + [1] * 3, 2) == [-1, -1, 40000, 60000, 60000, 60000, 40000, -1, -1]
assert sol.getAverages([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 4) == [-1, -1, -1, -1, 5, 6, -1, -1, -1, -1]
