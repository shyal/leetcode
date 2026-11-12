# URL: https://leetcode.com/problems/longest-balanced-substring-i/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 3713. Longest Balanced Substring I
#
# You are given a string s consisting of lowercase English letters.
#
# A substring of s is called balanced if all distinct characters in the substring appear the same number of times.
#
# Return the length of the longest balanced substring of s.
#
# Example 1:
#
# Input: s = "abbac"
# Output: 4
# Explanation:
# The longest balanced substring is "abba" because both distinct characters 'a' and 'b' each appear exactly 2 times.
#
# Example 2:
#
# Input: s = "zzabccy"
# Output: 4
# Explanation:
# The longest balanced substring is "zabc" because the distinct characters 'z', 'a', 'b', and 'c' each appear exactly 1 time.
#
# Example 3:
#
# Input: s = "aba"
# Output: 2
# Explanation:
# One of the longest balanced substrings is "ab" because both distinct characters 'a' and 'b' each appear exactly 1 time. Another longest balanced substring is "ba".
#
# Constraints:
#
#     1 <= s.length <= 1000
#     s consists of lowercase English letters.
#
# ---
# 
# class Solution
#   def longestBalanced(s: str) -> int
#     ret res = 0
#     for ss in substrings(s)
#       if len(set(counter(ss).values())) == 1
#         res = max(len(ss), res)
# LEETCODE: Accepted (3229 ms, 19.1 MB)



# mu 0.17

class Solution
  def longestBalanced(s: str) -> int
    ret res = 0
    for i in 0..<len(s)
      c = counter()
      for j in i..<len(s)
        c[s[j]] += 1
        if len(set(c.values())) == 1
          res = max(res, j - i + 1)


sol = Solution()

print(sol.longestBalanced('abbac'))  # 4

assert sol.longestBalanced('abbac') == 4
assert sol.longestBalanced('zzabccy') == 4
assert sol.longestBalanced('aba') == 2
assert sol.longestBalanced('a') == 1
assert sol.longestBalanced('aa') == 2
assert sol.longestBalanced('abcabcabc') == 9
assert sol.longestBalanced('aabbccddeeffgg') == 14
assert sol.longestBalanced('abcdeffedcba') == 12
assert sol.longestBalanced('zzzzzzzzzz') == 10
assert sol.longestBalanced('ababababab') == 10
assert sol.longestBalanced('a' * 500 + 'b' * 500) == 1000
assert sol.longestBalanced('a' * 333 + 'b' * 333 + 'c' * 334) == 999
assert sol.longestBalanced('abcdefghijklmnopqrstuvwxyz' * 38 + 'abc') == 988
assert sol.longestBalanced('a' * 999 + 'b') == 999
assert sol.longestBalanced('a' * 1000) == 1000
