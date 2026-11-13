# URL: https://leetcode.com/problems/longest-harmonious-subsequence/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 594. Longest Harmonious Subsequence
#
# We define a harmonious array as an array where the difference between its maximum value and its minimum value is exactly 1.
#
# Given an integer array nums, return the length of its longest harmonious subsequence among all its possible subsequences.
#
# Example 1:
#
# Input: nums = [1,3,2,2,5,2,3,7]
# Output: 5
# Explanation:
# The longest harmonious subsequence is [3,2,2,2,3].
#
# Example 2:
#
# Input: nums = [1,2,3,4]
# Output: 2
# Explanation:
# The longest harmonious subsequences are [1,2], [2,3], and [3,4], all of which have a length of 2.
#
# Example 3:
#
# Input: nums = [1,1,1,1]
# Output: 0
# Explanation:
# No harmonic subsequence exists.
#
# Constraints:
#
#     1 <= nums.length <= 2 * 10^4
#     -10^9 <= nums[i] <= 10^9
#
# ---
# STAGE 1 of 3 - the approach. Write it in plain English under this line. Then run make solved.
#
# For each number x in nums, loop over the whole array again and count the numbers equal to x or x + 1 (only if x + 1 is there). The largest count is the answer.

# mu 0.17

class Solution
  def solve(x)
    pass

sol = Solution()
