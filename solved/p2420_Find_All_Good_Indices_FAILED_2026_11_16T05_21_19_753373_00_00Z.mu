# URL: https://leetcode.com/problems/find-all-good-indices/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 2420. Find All Good Indices
#
# You are given a 0-indexed integer array nums of size n and a positive integer k.
#
# We call an index i in the range k <= i < n - k good if the following conditions are satisfied:
#
# - The k elements that are just before the index i are in non-increasing order.
# - The k elements that are just after the index i are in non-decreasing order.
#
# Return an array of all good indices sorted in increasing order.
#
# Example 1:
#
# Input: nums = [2,1,1,1,3,4,1], k = 2
# Output: [2,3]
# Explanation: There are two good indices in the array:
# - Index 2. The subarray [2,1] is in non-increasing order, and the subarray [1,3] is in non-decreasing order.
# - Index 3. The subarray [1,1] is in non-increasing order, and the subarray [3,4] is in non-decreasing order.
# Note that the index 4 is not good because [4,1] is not non-decreasing.
#
# Example 2:
#
# Input: nums = [2,1,1,2], k = 2
# Output: []
# Explanation: There are no good indices in this array.
#
# Constraints:
#
#     n == nums.length
#     3 <= n <= 10^5
#     1 <= nums[i] <= 10^6
#     1 <= k <= n / 2
#
# ---
# STAGE 1 of 3 - the approach. Write it in plain English under this line. Then run make solved.
#

# mu 0.18


class Solution
  def goodIndices(nums: [int], k: int) -> [int]
    left = []
    count = 1
    min_count = inf
    for >i in 0..<len nums
      if i > 0 and nums[i-1] >= nums[i]
        count += 1
      else
        count = 1
      min_count = min(count, min_count)
      left <- min_count
    count = 1
    right = []
    min_count = inf
    for i in range(len(nums)-1, -1, -1)
      if i < len(nums) -1 and nums[i+1] >= nums[i]
        count += 1
      else
        count = 1
      min_count = min(min_count, count)
      right <- min_count
    right = right[::-1]
    print('     ', nums)
    print('left ', left)
    print('right', right)
    ret res = []
    for >i in 1..<len(nums)-1
      if k in left[:i] and k in right[i+1:]
        res <- i


    

sol = Solution()

print(sol.goodIndices([5, 4, 3, 2, 1, 2, 3, 4, 5], 2)) # 3, 4, 5

# assert sol.goodIndices([2, 1, 1, 1, 3, 4, 1], 2) == [2, 3]
# assert sol.goodIndices([2, 1, 1, 2], 2) == []
# assert sol.goodIndices([1, 1, 1, 1, 1, 1, 1], 3) == [3]
# assert sol.goodIndices([5, 4, 3, 2, 1, 2, 3, 4, 5], 2) == [3, 4, 5]
# assert sol.goodIndices([1, 2, 3, 4, 5, 4, 3, 2, 1], 2) == []
# assert sol.goodIndices([3, 3, 3, 3, 3, 3, 3], 3) == [3]
# # assert sol.goodIndices([10 ** 6] * 10 ** 5, 50000) == []
# # assert sol.goodIndices([1, 2, 3, 4, 5], 1) == [1, 2, 3]
# # assert sol.goodIndices([5, 4, 3, 2, 1], 1) == [1, 2, 3]
# # assert sol.goodIndices([1, 2, 2, 2, 3, 4, 4, 4, 5], 3) == [4]
# # assert sol.goodIndices([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 4) == []
# # assert sol.goodIndices([10, 9, 8, 7, 6, 5, 4, 3, 2, 1], 4) == []
# # assert sol.goodIndices([1, 3, 2, 4, 3, 5, 4, 6, 5, 7], 2) == [3, 5, 7]
# # assert sol.goodIndices([2, 2, 2, 2, 2, 2, 2, 2, 2, 2], 5) == []


# FAILED: walked away after 45m 43s; no working solution.
# Judge the move the defect is in as struggled, not clean. A move the code never reached gets no verdict.
