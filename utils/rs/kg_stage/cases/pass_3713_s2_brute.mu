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
# STAGE 1 of 3 - the approach. Write it in plain English under this line. Then run make solved.
#
# two loops, counter grows with j, check all counts equal
# STAGE 1: pass
# STAGE 2 of 3 - the pseudocode. Write one comment line for each step in the solve below. Then run make solved.

# mu 0.17

class Solution
  def solve(x)
    # res = 0
    # for i in 0 to len s
      # c = counter
      # for j in i to len s
        # c[s[j]] += 1
        # if len(set(c.values())) == 1
          # res = max(res, j - i + 1)
    # return res
    pass

sol = Solution()
