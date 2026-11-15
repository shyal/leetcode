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
# STAGE 1 of 3 - the approach. Write it in plain English under this line. Then run make solved.
# print(sol.longestSubsequence([1, 2, 3, 4, 5], 2))
# 
# 1: 1,
# 2: 1,
# 3: 2, asking for D[v - diff] (1) had a hit in the dict, so we set the value of 3 to 2
# 4: 2, asking for D[v - diff] (2) had a hit in the dict, so we set the value of 4 to 2
# 5: 3, asking for D[v - diff] (3) had a hit of 2 in the dict, so we set the value of 5 to 3
# LEETCODE: Accepted (82 ms, 31.4 MB)


# mu 0.18

class Solution
  def longestSubsequence(arr: [int], difference: int) -> int
    D = {:int}
    for >i, v in arr
      D[v] = max(D[v], D[v - difference] + 1)
    D ? max(D.values()) : 0


sol = Solution()

print(sol.longestSubsequence([1, 2, 3, 4, 5], 2))

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
