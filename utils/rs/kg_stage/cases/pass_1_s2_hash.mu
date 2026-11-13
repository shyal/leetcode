# URL: https://leetcode.com/problems/two-sum/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 1. Two Sum
#
# You are given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.
#
# You may assume that each input would have exactly one solution, and you may not use the same element twice.
#
# You can return the answer in any order.
#
# Example 1:
#
# Input: nums = [2,7,11,15], target = 9
# Output: [0,1]
# Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
#
# Example 2:
#
# Input: nums = [3,2,4], target = 6
# Output: [1,2]
#
# Example 3:
#
# Input: nums = [3,3], target = 6
# Output: [0,1]
#
# Constraints:
#
#     2 <= nums.length <= 10^4
#     -10^9 <= nums[i] <= 10^9
#     -10^9 <= target <= 10^9
#     Only one valid answer exists.
#
# Follow-up: Can you come up with an algorithm that is less than O(n^2) time complexity?
#
# ---
# STAGE 1 of 3 - the approach. Write it in plain English under this line. Then run make solved.
#
# dict of seen values
# STAGE 1: pass
# STAGE 2 of 3 - the pseudocode. Write one comment line for each step in the solve below. Then run make solved.

# mu 0.17

class Solution
  def solve(x)
    # seen = {}
    # for i, x in nums
      # if target - x in seen
        # return [seen[target - x], i]
      # seen[x] = i
    pass

sol = Solution()
