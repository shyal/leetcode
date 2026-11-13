# URL: https://leetcode.com/problems/3sum/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 15. 3Sum
#
# Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.
#
# Notice that the solution set must not contain duplicate triplets.
#
# Example 1:
#
# Input: nums = [-1,0,1,2,-1,-4]
# Output: [[-1,-1,2],[-1,0,1]]
# Explanation:
# nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0.
# nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0.
# nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0.
# The distinct triplets are [-1,0,1] and [-1,-1,2].
# Notice that the order of the output and the order of the triplets does not matter.
#
# Example 2:
#
# Input: nums = [0,1,1]
# Output: []
# Explanation: The only possible triplet does not sum up to 0.
#
# Example 3:
#
# Input: nums = [0,0,0]
# Output: [[0,0,0]]
# Explanation: The only possible triplet sums up to 0.
#
# Constraints:
#
#     3 <= nums.length <= 3000
#     -10^5 <= nums[i] <= 10^5
#
# ---
# STAGE 1 of 3 - the approach. Write it in plain English under this line. Then run make solved.
#
# three loops
# STAGE 1: pass
# STAGE 2 of 3 - the pseudocode. Write one comment line for each step in the solve below. Then run make solved.

# mu 0.17

class Solution
  def solve(x)
    # res = set
    # for i in 0 to n
      # for j in i+1 to n
        # for k in j+1 to n
          # if nums[i] + nums[j] + nums[k] == 0
            # add sorted triple to res
    # return list of res
    pass

sol = Solution()
