# URL: https://leetcode.com/problems/house-robber-v/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 3840. House Robber V
#
# You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed and is protected by a security system with a color code.
#
# You are given two integer arrays nums and colors, both of length n, where nums[i] is the amount of money in the i-th house and colors[i] is the color code of that house.
#
# You cannot rob two adjacent houses if they share the same color code.
#
# Return the maximum amount of money you can rob.
#
# Example 1:
#
# Input: nums = [1,4,3,5], colors = [1,1,2,2]
# Output: 9
# Explanation:
# - Choose houses i = 1 with nums[1] = 4 and i = 3 with nums[3] = 5 because they are non-adjacent.
# - Thus, the total amount robbed is 4 + 5 = 9.
#
# Example 2:
#
# Input: nums = [3,1,2,4], colors = [2,3,2,2]
# Output: 8
# Explanation:
# - Choose houses i = 0 with nums[0] = 3, i = 1 with nums[1] = 1, and i = 3 with nums[3] = 4.
# - This selection is valid because houses i = 0 and i = 1 have different colors, and house i = 3 is non-adjacent to i = 1.
# - Thus, the total amount robbed is 3 + 1 + 4 = 8.
#
# Example 3:
#
# Input: nums = [10,1,3,9], colors = [1,1,1,2]
# Output: 22
# Explanation:
# - Choose houses i = 0 with nums[0] = 10, i = 2 with nums[2] = 3, and i = 3 with nums[3] = 9.
# - This selection is valid because houses i = 0 and i = 2 are non-adjacent, and houses i = 2 and i = 3 have different colors.
# - Thus, the total amount robbed is 10 + 3 + 9 = 22.
#
# Constraints:
#
#     1 <= n == nums.length == colors.length <= 10^5
#     1 <= nums[i], colors[i] <= 10^5
#
# ---
# STAGE 1 of 3 - the approach. Write it in plain English under this line. Then run make solved.
# DP problem.
# 
#          
# nums =   [10,1,3,9]
#           x   x  x  -> 22
# colors = [1, 1,1,2]
# 
# 
# [1, 2, 3, 4, 5],
#  x     x     x  -> 9
# [1, 1, 1, 1, 1]
# 
# 
# [1, 1, 1, 1, 1, 1]
#     x     x     x   -> 6
# [1, 2, 1, 2, 1, 2]
# 
# 
# The only real constraint is within adjacent houses in the same group, so we need to find a case that
# doesn't allow a greedy selection. Greedy would be to start with the max house:
# 
#  x   x
# 10 9 7 9
# and here we have it. picking the max house is sub-optimal, because 9 9 was the better pick.
# And this is where the DP comes in. Our choice, within groups, is to pick between the two max
# values, then recursively visiting all the allowed houses in the group to find the max value.
# 
# Do that for all coloured groups, and everything up.
# STAGE 1: pass
# STAGE 2 of 3 - the pseudocode. Write one comment line for each step in the solve below. Then run make solved.



# mu 0.18

class Solution
  def rob(nums: [int], colors: [int]) -> int
    n = len nums
    last = None
    ret res = 0
    for >i, v in nums
      if colors[i] != last
        print("invoking memo")
        r = memo {
          (i, g) ->
            if i >= n
              return 0
            if colors[i] != g
              return 0
            a = nums[i] + mu(i + 2, g)
            print('a', a)
            b = mu(i + 1, g)
            max(a, b)
        }(i, colors[i])
        print(r)
        res += r
      last = colors[i]

sol = Solution()


sol.rob([3, 1, 2, 4], [2, 3, 2, 2])


# print(sol.rob([1, 4, 3, 5], [1, 1, 2, 2]))  # 9

# assert sol.rob([1, 4, 3, 5], [1, 1, 2, 2]) == 9
# assert sol.rob([3, 1, 2, 4], [2, 3, 2, 2]) == 8
# assert sol.rob([10, 1, 3, 9], [1, 1, 1, 2]) == 22

# assert sol.rob([1], [1]) == 1
# assert sol.rob([5, 5, 5, 5], [1, 1, 1, 1]) == 10
# assert sol.rob([5, 5, 5, 5], [1, 2, 1, 2]) == 20
# assert sol.rob([1, 2, 3, 4, 5], [1, 1, 1, 1, 1]) == 9
# assert sol.rob([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]) == 15
# assert sol.rob([100000] * 100000, [1] * 100000) == 5000000000
# assert sol.rob([1] * 100000, list(1..<100001)) == 100000
# assert sol.rob([1, 2, 3, 4, 5], [1, 1, 2, 2, 3]) == 11
# assert sol.rob([10, 1, 10, 1, 10], [1, 2, 1, 2, 1]) == 32
# assert sol.rob([10, 10, 10, 10, 10], [1, 1, 2, 2, 1]) == 30
# assert sol.rob([1, 2, 3, 4, 5, 6], [1, 2, 2, 3, 3, 4]) == 15
# assert sol.rob([1, 1, 1, 1, 1, 1], [1, 2, 1, 2, 1, 2]) == 6


# FAILED: walked away after 36m 46s; no working solution.
# Judge the move the defect is in as struggled, not clean. A move the code never reached gets no verdict.
