# URL: https://leetcode.com/problems/running-sum-of-1d-array/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 1480. Running Sum of 1d Array
#
# Given an array nums. We define a running sum of an array as runningSum[i] = sum(nums[0]…nums[i]).
#
# Return the running sum of nums.
#
# Example 1:
#
# Input: nums = [1,2,3,4]
# Output: [1,3,6,10]
# Explanation: Running sum is obtained as follows: [1, 1+2, 1+2+3, 1+2+3+4].
#
# Example 2:
#
# Input: nums = [1,1,1,1,1]
# Output: [1,2,3,4,5]
# Explanation: Running sum is obtained as follows: [1, 1+1, 1+1+1, 1+1+1+1, 1+1+1+1+1].
#
# Example 3:
#
# Input: nums = [3,1,2,10,1]
# Output: [3,4,6,16,17]
#
# Constraints:
#
#     1 <= nums.length <= 1000
#     -10^6 <= nums[i] <= 10^6
#
# ---
# LEETCODE: Accepted (0 ms, 19.2 MB)

# mu 0.13

class Solution
  def runningSum(nums: [int]) -> [int]
    [*scan(+, nums)]

sol = Solution()

print(sol.runningSum([1, 2, 3, 4]))  # [1,3,6,10]

assert sol.runningSum([1, 2, 3, 4]) == [1, 3, 6, 10]
assert sol.runningSum([1, 1, 1, 1, 1]) == [1, 2, 3, 4, 5]
assert sol.runningSum([3, 1, 2, 10, 1]) == [3, 4, 6, 16, 17]

assert sol.runningSum([0]) == [0]
assert sol.runningSum([-1, -2, -3, -4]) == [-1, -3, -6, -10]
assert sol.runningSum([5]) == [5]
assert sol.runningSum([1, 2, 2, 2, 3]) == [1, 3, 5, 7, 10]
assert sol.runningSum([1000]) == [1000]
assert sol.runningSum([10 ** 6, -10 ** 6, 10 ** 6, -10 ** 6]) == [1000000, 0, 1000000, 0]
assert sol.runningSum([-10 ** 6, 10 ** 6, -10 ** 6, 10 ** 6]) == [-1000000, 0, -1000000, 0]
