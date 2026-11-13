# URL: https://leetcode.com/problems/longest-substring-without-repeating-characters/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 3. Longest Substring Without Repeating Characters
#
# Given a string s, find the length of the longest substring without duplicate characters.
#
# Example 1:
#
# Input: s = "abcabcbb"
# Output: 3
# Explanation: The answer is "abc", with the length of 3. Note that "bca" and "cab" are also correct answers.
#
# Example 2:
#
# Input: s = "bbbbb"
# Output: 1
# Explanation: The answer is "b", with the length of 1.
#
# Example 3:
#
# Input: s = "pwwkew"
# Output: 3
# Explanation: The answer is "wke", with the length of 3.
# Notice that the answer must be a substring, "pwke" is a subsequence and not a substring.
#
# Constraints:
#
#     0 <= s.length <= 10^5
#     s consists of English letters, digits, symbols and spaces.
#
# ---
# STAGE 1 of 3 - the approach. Write it in plain English under this line. Then run make solved.
#
# Try every substring with two loops over start and end. For each one put its letters in a set and check that the size of the set equals the length. Keep the longest.

# mu 0.17

class Solution
  def solve(x)
    pass

sol = Solution()
