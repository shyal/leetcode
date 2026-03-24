"""
URL: https://leetcode.com/problems/is-subsequence/description/?envType=problem-list-v2&envId=vn57k9wr

392. Is Subsequence

Given two strings s and t, return true if s is a subsequence of t, or false otherwise.

A subsequence of a string is a new string that is formed from the original string by deleting some (can be none) of the characters without disturbing the relative positions of the remaining characters. (i.e., "ace" is a subsequence of "abcde" while "aec" is not).

Example 1:

Input: s = "abc", t = "ahbgdc"
Output: true

Example 2:

Input: s = "axc", t = "ahbgdc"
Output: false

Constraints:

    0 <= s.length <= 100
    0 <= t.length <= 10^4
    s and t consist only of lowercase English letters.

Follow up: Suppose there are lots of incoming s, say s1, s2, ..., sk where k >= 10^9, and you want to check one by one to see if t has its subsequence. In this scenario, how would you change your code?
"""


class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        a = 0
        counts = 0
        for b in range(len(t)):
            if a == len(s):
                return True
            if s[a] == t[b]:
                counts += 1
                a += 1
        return a == len(s)


sol = Solution()

# print(sol.isSubsequence("abc", "ahbgdc"))  # true

assert sol.isSubsequence("abc", "ahbgdc") == True
assert sol.isSubsequence("axc", "ahbgdc") == False
assert sol.isSubsequence("", "ahbgdc") == True
assert sol.isSubsequence("", "") == True
assert sol.isSubsequence("a", "") == False
assert sol.isSubsequence("abc", "abc") == True
assert sol.isSubsequence("aa", "a") == False
assert sol.isSubsequence("aa", "aaa") == True
assert sol.isSubsequence("ab", "aabb") == True
assert sol.isSubsequence("abc", "abbbc") == True
assert sol.isSubsequence("abc", "abbb") == False
assert sol.isSubsequence("xyz", "abc") == False
assert sol.isSubsequence("ace", "abcde") == True
assert sol.isSubsequence("aec", "abcde") == False
assert sol.isSubsequence("a", "a") == True
assert sol.isSubsequence("a", "b") == False