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
# User a counter: look at the 2 maximum frequencies that have a delta of 1 in their values.
# 
# [1,3,2,2,5,2,3,7]
# 
# 
# 1: 1, 3: 2, 2: 3: 5: 1: 7: 1
# 
# the two max frequencies are 3 and 2
# 
# 
# [1,2,3,4]
# 
# all have frequencies of 1, so the 2 max with a delta of 1 are any pair.
# 
# 
# [2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5]
# 
# {2: 3, 3: 3, 4: 3, 5: 3}
# 
# any 2 will do
# 
# 1, 1, 1, 1, 1, 1, 9, 9, 9, 9, 9, 9, 9, 3, 3, 4, 4
# 
# {1: 6, 9: 7, 3: 2, 4: 2}
# 
# 
# 
# 
# STAGE 1: pass
# STAGE 2 of 3 - the pseudocode. Write one comment line for each step in the solve below. Then run make solved.
# STAGE 2: pass
# class Solution
#   def findLHS(nums: [int]) -> int
#     # create a counter
#     # res = 0
#     # for each key in the counter (sorted asc)
#       # if there is a key with the value + 1
#         # res = max(res, the sum of their frequencies)
#     # return res
#     pass
# STAGE 3 of 3 - the code. Replace each pseudocode line with code. Then run make solved.
# LEETCODE: Accepted (41 ms, 20.8 MB)

# mu 0.17

class Solution
  def findLHS(nums: [int]) -> int
    cnt = counter(nums)
    ret res = 0
    for k in sorted(cnt)
      if cnt[k + 1]
        res = max(res, cnt[k] + cnt[k + 1])

sol = Solution()

print(sol.findLHS([1, 3, 2, 2, 5, 2, 3, 7]))  # 5

assert sol.findLHS([1, 3, 2, 2, 5, 2, 3, 7]) == 5
assert sol.findLHS([1, 2, 3, 4]) == 2
assert sol.findLHS([1, 1, 1, 1]) == 0
assert sol.findLHS([]) == 0
assert sol.findLHS([1]) == 0
assert sol.findLHS([1, 1, 1, 1, 1]) == 0
assert sol.findLHS([1, 2]) == 2
assert sol.findLHS([1, 2, 2, 3, 3, 4, 4, 5, 5]) == 4
assert sol.findLHS([-1, -1, 0, 0, 1, 1]) == 4
assert sol.findLHS([-10 ** 9, -10 ** 9 + 1, 0, 10 ** 9 - 1, 10 ** 9]) == 2
assert sol.findLHS([5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 7]) == 9
assert sol.findLHS([100, 101, 101, 102, 102, 102, 103]) == 5
assert sol.findLHS([0] * 10000 + [1] * 10000) == 20000
assert sol.findLHS([1, 3, 5, 7, 9]) == 0
assert sol.findLHS([2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5]) == 6
