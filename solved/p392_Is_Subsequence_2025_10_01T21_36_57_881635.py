"""
392. Is Subsequence
Solved
Easy
Topics
premium lock icon
Companies
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
0 <= t.length <= 104
s and t consist only of lowercase English letters.
 

Follow up: Suppose there are lots of incoming s, say s1, s2, ..., sk where k >= 109, and you want to check one by one to see if t has its subsequence. In this scenario, how would you change your code?
"""


class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        if not s:
            return True
        i = 0
        for c in t:
            if s[i] == c:
                i += 1
            if i == len(s):
                return True
        return False


sol = Solution()

assert sol.isSubsequence(s="abc", t="ahbgdc") == True
assert sol.isSubsequence(s="axc", t="ahbgdc") == False
assert sol.isSubsequence(s="", t="ahbgdc") == True
assert sol.isSubsequence(s="a", t="") == False
assert sol.isSubsequence(s="", t="") == True
assert sol.isSubsequence(s="abc", t="ab") == False
assert sol.isSubsequence(s="leetcode", t="leetcode") == True
assert sol.isSubsequence(s="g", t="ahbgdc") == True
assert sol.isSubsequence(s="z", t="ahbgdc") == False
assert sol.isSubsequence(s="abc", t="aebdc") == True
assert sol.isSubsequence(s="cba", t="ahbgdc") == False
assert sol.isSubsequence(s="aaa", t="aa") == False
assert sol.isSubsequence(s="aaa", t="aaaaa") == True
assert sol.isSubsequence(s="dc", t="ahbgdc") == True
big_t = "a" * 5000 + "b" + "c" * 5000
assert sol.isSubsequence(s="abc", t=big_t) == True
big_s = "a" * 100 + "z"
big_t = "a" * 10000
assert sol.isSubsequence(s=big_s, t=big_t) == False

