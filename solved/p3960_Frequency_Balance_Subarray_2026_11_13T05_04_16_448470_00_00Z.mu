# URL: https://leetcode.com/problems/frequency-balance-subarray/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 3960. Frequency Balance Subarray
#
# You are given an integer array nums.
#
# Define a frequency balance subarray as follows:
#
# - If the subarray contains only one distinct value, it is frequency balanced.
# - Otherwise, there must exist a positive integer f such that every distinct value in the subarray occurs either f or 2 * f times, and both frequencies occur among the distinct values.
#
# Return an integer denoting the length of the longest frequency balance subarray.
#
# Example 1:
#
# Input: nums = [1,2,2,1,2,3,3,3]
# Output: 5
# Explanation:
# - The longest frequency balance subarray is [2, 1, 2, 3, 3].
# - The elements that appear most frequently are 2 and 3, both appearing twice.
# - The remaining element 1 appears once, meeting the requirements.
#
# Example 2:
#
# Input: nums = [5,5,5,5]
# Output: 4
# Explanation:
# - The longest frequency balance subarray is [5, 5, 5, 5].
# - The element that appears most frequently is 5.
# - There are no other elements meeting the requirements.
#
# Example 3:
#
# Input: nums = [1,2,3,4]
# Output: 1
# Explanation:
# Since all elements appear only once, the length of the longest frequency balance subarray is 1.
#
# Constraints:
#
#     1 <= nums.length <= 10^3
#     1 <= nums[i] <= 10^9
#
# ---
# STAGE 1 of 3 - the approach. Write it in plain English under this line. Then run make solved.
#
# ok so we're looking for a subarray with frequencies that have this property. There's a pos int f, and the frequencies in the subarray (the values of a counter) have f and 2f. But the length of the subarray needs to be maximized.
# 
# the brute force method might be fine here, since the constraints are managable: 10**3. 
# 
# So a double for loop. Build the counter as you go, and check if there's an f and 2f. Do this by iterating over the values of the counter.
# STAGE 1: pass
# STAGE 2 of 3 - the pseudocode. Write one comment line for each step in the solve below. Then run make solved.
# STAGE 2: miss
# STAGE 2: miss
# STAGE 2: miss
# STAGE 2: pass
# class Solution
#   def getLength(nums: [int]) -> int
#     # if len(set(nums)) == 1
#       # return nums[0]
#     # res = 0
#     # for i in len nums -1
#       # cnt = counter()# {2: 2, 1: 1, 3: 2}
#       # for j in i to len nums -1
#         # cnt[nums[j]] += 1
#         # vals = set(cnt.values()) # 1, 2
#         # for f in vals
#           # if 2f in vals
#             # res = max(res, j - i + 1)
#     # return res
#     pass
# STAGE 3 of 3 - the code. Replace each pseudocode line with code. Then run make solved.
# 
#  this gives a TLE:
# 
# class Solution
#   def getLength(nums: [int]) -> int
#     if len(set(nums)) == 1
#       return len(nums)
#     res = 1
#     for >i in nums
#       cnt = counter()
#       for j in i..<len nums
#         cnt[nums[j]] += 1
#         vals = set(cnt.values())
#         if len vals == 2
#           good = true
#           for f in vals
#             if not (2f in vals or (f // 2 in vals if f % 2 == 0 else false))
#               good = false
#               break
#           if good
#             res = max(res, j - i + 1)
#           elif len vals > 2
#             break
#     return res
# 
# LEETCODE: Time Limit Exceeded (910/922 cases)




# mu 0.17

class Solution
  def getLength(nums: [int]) -> int
    if len(set(nums)) == 1
      return len(nums)
    res = 1
    for >i in nums
      cnt = counter()
      for j in i..<len nums
        cnt[nums[j]] += 1
        vals = set(cnt.values())
        if len vals == 2
          good = true
          for f in vals
            if not (2f in vals or (f // 2 in vals if f % 2 == 0 else false))
              good = false
              break
          if good
            res = max(res, j - i + 1)
          elif len vals > 2
            break
    return res

sol = Solution()

print(sol.getLength([1, 2, 2, 1, 2, 3, 3, 3]))  # 5

assert sol.getLength([1, 2, 2, 1, 2, 3, 3, 3]) == 5
assert sol.getLength([5, 5, 5, 5]) == 4
assert sol.getLength([1, 2, 3, 4]) == 1
assert Solution().getLength([1]) == 1
assert Solution().getLength([2, 2, 2, 2, 2]) == 5
assert Solution().getLength([1, 1, 2, 2, 2, 2]) == 6
assert Solution().getLength([3, 3, 3, 6, 6, 6, 6]) == 6
assert Solution().getLength([1, 2, 2, 4, 4, 4, 4, 4, 4]) == 6
assert Solution().getLength([1, 1, 1, 2, 2, 2, 2, 2, 2, 2]) == 9
assert Solution().getLength([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) == 1
assert Solution().getLength([1, 1, 2, 2, 3, 3, 3, 3, 3, 3]) == 8
assert Solution().getLength([10 ** 9, 10 ** 9, 10 ** 9, 10 ** 9, 10 ** 9]) == 5
assert Solution().getLength([1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2]) == 6
assert Solution().getLength([1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 3, 3]) == 12
assert Solution().getLength([1] * 500 + [2] * 1000) == 1500
