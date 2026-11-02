# URL: https://leetcode.com/problems/longest-arithmetic-subsequence-of-given-difference/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 1218. Longest Arithmetic Subsequence of Given Difference
#
# Given an integer array arr and an integer difference, return the length of the longest subsequence in arr which is an arithmetic sequence such that the difference between adjacent elements in the subsequence equals difference.
#
# A subsequence is a sequence that can be derived from arr by deleting some or no elements without changing the order of the remaining elements.
#
# Example 1:
#
# Input: arr = [1,2,3,4], difference = 1
# Output: 4
# Explanation: The longest arithmetic subsequence is [1,2,3,4].
#
# Example 2:
#
# Input: arr = [1,3,5,7], difference = 1
# Output: 1
# Explanation: The longest arithmetic subsequence is any single element.
#
# Example 3:
#
# Input: arr = [1,5,7,8,5,3,4,2,1], difference = -2
# Output: 4
# Explanation: The longest arithmetic subsequence is [7,5,3,1].
#
# Constraints:
#
#     1 <= arr.length <= 10^5
#     -10^4 <= arr[i], difference <= 10^4
#
# ---
# n square solution:
# 
# class Solution
#   def longestSubsequence(arr: [int], difference: int) -> int
#     DP = table(len(arr), fill=1)
#     for j, i in pairs(len(arr), back=true)
#       if arr[j] + difference == arr[i]
#         DP[i] = max(DP[j] + 1, DP[i])
#     max(DP) if DP else 0
# 
# Learning

# mu 0.16

class Solution
  def longestSubsequence(arr: [int], k: int) -> int
    dp = {}
    for x in arr
      dp[x] = dp.get(x - k, 0) + 1
    max(dp.values()) if dp else 0

sol = Solution()

print(sol.longestSubsequence([1, 2, 3, 4], 1))  # 4

assert sol.longestSubsequence([1, 2, 3, 4], 1) == 4
assert sol.longestSubsequence([1, 3, 5, 7], 1) == 1
assert sol.longestSubsequence([1, 5, 7, 8, 5, 3, 4, 2, 1], -2) == 4
assert sol.longestSubsequence([], 1) == 0
assert sol.longestSubsequence([5], 0) == 1
assert sol.longestSubsequence([2, 2, 2, 2], 0) == 4
assert sol.longestSubsequence([1, 3, 5, 7, 9, 11, 13, 15], 2) == 8
assert sol.longestSubsequence([10 ** 4, 10 ** 4 - 1, 10 ** 4 - 2], -1) == 3
assert sol.longestSubsequence([-10 ** 4, -9999, -9998], 1) == 3
assert sol.longestSubsequence([1, 1, 2, 2, 3, 3, 4, 4], 1) == 4
assert sol.longestSubsequence([1] * 10 ** 5, 0) == 100000
assert sol.longestSubsequence(list(0..<10 ** 5), 1) == 100000
assert sol.longestSubsequence(list(range(10 ** 5, 0, -1)), -1) == 100000
assert sol.longestSubsequence([0, -1, -2, -3, -4], -1) == 5
assert sol.longestSubsequence([1, 10000, 20000, 30000], 10000) == 3


# FAILED: walked away after 45m 41s; no working solution.
# Judge the move the defect is in as struggled, not clean. A move the code never reached gets no verdict.
