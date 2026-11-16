# REFERENCE: d540 Longest Subsequence of Consecutive Integers
class Solution
  def longestSubsequence(arr: [int]) -> int
    longest = {}
    for x in arr
      longest[x] = longest.get(x - 1, 0) + 1
    max(longest.values())
