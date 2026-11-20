# URL: https://leetcode.com/problems/count-the-number-of-fair-pairs/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 2563. Count the Number of Fair Pairs
#
# Given a 0-indexed integer array nums of size n and two integers lower and upper, return the number of fair pairs.
#
# A pair (i, j) is fair if:
#
#     0 <= i < j < n, and
#     lower <= nums[i] + nums[j] <= upper
#
#
# Example 1:
#
# Input: nums = [0,1,7,4,4,5], lower = 3, upper = 6
# Output: 6
# Explanation: There are 6 fair pairs: (0,3), (0,4), (0,5), (1,3), (1,4), and (1,5).
#
# Example 2:
#
# Input: nums = [1,7,9,2,5], lower = 11, upper = 11
# Output: 1
# Explanation: There is a single fair pair: (2,3).
#
#
# Constraints:
#
#     1 <= nums.length <= 10^5
#     nums.length == n
#     -10^9 <= nums[i] <= 10^9
#     -10^9 <= lower <= upper <= 10^9
#
# ---
# Hint 1: it's ok to sort
# Built a drill for pairs at most drill, and grated
# learning

class Solution
  def countFairPairs(nums: [int], lower: int, upper: int) -> int
    nums.sort()
    def pairs_at_most(x)
      count, left, right = 0, 0, len(nums) - 1
      while left < right
        if nums[left] + nums[right] <= x
          count += right - left
          left += 1
        else
          right -= 1
      count
    pairs_at_most(upper) - pairs_at_most(lower - 1)


sol = Solution()

print(sol.countFairPairs([1, 7, 9, 2, 5], 11, 11))


assert sol.countFairPairs([0, 1, 7, 4, 4, 5], 3, 6) == 6
assert sol.countFairPairs([1, 7, 9, 2, 5], 11, 11) == 1
assert sol.countFairPairs([], 0, 0) == 0
assert sol.countFairPairs([1], 0, 2) == 0
assert sol.countFairPairs([1, 1, 1, 1], 2, 2) == 6
assert sol.countFairPairs([-10 ** 9, 10 ** 9], -10 ** 9, 10 ** 9) == 1
assert sol.countFairPairs([10 ** 9, 10 ** 9, 10 ** 9], 2 * 10 ** 9, 2 * 10 ** 9) == 3
assert sol.countFairPairs([-1, -2, -3, -4], -5, -3) == 4
assert sol.countFairPairs([0] * 100000, 0, 0) == 4999950000
assert sol.countFairPairs(list(0..<100000), 0, 1) == 1
assert sol.countFairPairs([5, 5, 5, 5, 5], 10, 10) == 10
assert sol.countFairPairs([1, 2, 3, 4, 5], 8, 10) == 2
assert sol.countFairPairs([1, 2, 2, 2, 3], 4, 5) == 7
assert sol.countFairPairs([-5, 0, 5, 10], 5, 15) == 4
