# URL: https://leetcode.com/problems/palindromic-substrings/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 647. Palindromic Substrings
#
# Given a string s, return the number of palindromic substrings in it.
#
# A string is a palindrome when it reads the same backward as forward.
#
# A substring is a contiguous sequence of characters within the string.
#
# Example 1:
#
# Input: s = "abc"
# Output: 3
# Explanation: Three palindromic strings: "a", "b", "c".
#
# Example 2:
#
# Input: s = "aaa"
# Output: 6
# Explanation: Six palindromic strings: "a", "a", "a", "aa", "aa", "aaa".
#
# Constraints:
#
#     1 <= s.length <= 1000
#     s consists of lowercase English letters.
#
# ---
# 
# 0 1 2 3
# a b b a
# length: 4
# 
# LEETCODE: Accepted (1202 ms, 223.4 MB)

# mu 0.13

class Solution
  def countSubstrings(s: str) -> int
    memo is_palindrome(s)
      if even(len(s))
        i = 0
        for a, b in zip(s, reversed(s))
          if i >= len(s) // 2
            return True
          if a != b
            return False
          i += 1
        return True
      if odd(len(s))
        start = (len(s) // 2)
        for i in 0..(len(s) // 2)
          a = s[start+i]
          b = s[start-i]
          if a != b
            return False
        return True
    ret res = 0
    for x in substrings(s)
      isp = is_palindrome(x)
      res += isp

sol = Solution()

print(sol.countSubstrings('abc'))  # 3

assert sol.countSubstrings('abc') == 3
assert sol.countSubstrings('aaa') == 6
assert sol.countSubstrings('') == 0
assert sol.countSubstrings('a') == 1
assert sol.countSubstrings('ab') == 2
assert sol.countSubstrings('aa') == 3
assert sol.countSubstrings('aba') == 4
assert sol.countSubstrings('abba') == 6
assert sol.countSubstrings('abcba') == 7
assert sol.countSubstrings('abcdedcba') == 13
assert sol.countSubstrings('a' * 1000) == 500500
assert sol.countSubstrings('ab' * 500) == 250500
assert sol.countSubstrings('abcde' * 200) == 1000
assert sol.countSubstrings('z' * 999 + 'y') == 499501
