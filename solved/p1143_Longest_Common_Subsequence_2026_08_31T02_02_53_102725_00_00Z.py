"""
URL: https://leetcode.com/problems/longest-common-subsequence/description/?envType=problem-list-v2&envId=vn57k9wr

1143. Longest Common Subsequence

Given two strings text1 and text2, return the length of their longest common subsequence. If there is no common subsequence, return 0.

A subsequence of a string is a new string generated from the original string with some characters (can be none) deleted without changing the relative order of the remaining characters.

For example, "ace" is a subsequence of "abcde".

A common subsequence of two strings is a subsequence that is common to both strings.

Example 1:

Input: text1 = "abcde", text2 = "ace"
Output: 3
Explanation: The longest common subsequence is "ace" and its length is 3.

Example 2:

Input: text1 = "abc", text2 = "abc"
Output: 3
Explanation: The longest common subsequence is "abc" and its length is 3.

Example 3:

Input: text1 = "abc", text2 = "def"
Output: 0
Explanation: There is no such common subsequence, so the result is 0.

Constraints:

    1 <= text1.length, text2.length <= 1000
    text1 and text2 consist of only lowercase English characters.

---

Wrote levenshtein distance.. then returned:

longest = len(text1) if len(text1) > len(text2) else len(text2)
h = helper(text1, text2)
return longest - h

Turns out it's:

h = helper(text1, text2)
return (len(text1) + len(text2) - h) // 2

Adding the length of both strings, subtracting the deletion distance, and dividing by 2,
which i couldn't figure out.

Also worth noting that i didn't figure out i had to remove the substitute part of levenshtein
to make it deletion distance.
"""


class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        @cache
        def helper(a, b):
            if len(a) == 0 or len(b) == 0:
                return len(a) or len(b)
            if a[-1] == b[-1]:
                return helper(a[:-1], b[:-1])
            dela = helper(a[:-1], b)
            delb = helper(a, b[:-1])
            return min([dela, delb]) + 1

        h = helper(text1, text2)
        return (len(text1) + len(text2) - h) // 2


sol = Solution()

# print(sol.longestCommonSubsequence("psnw", "vozsh"))  # 1
# print(sol.longestCommonSubsequence("abcde", "ace"))  # 3

assert sol.longestCommonSubsequence("abcde", "ace") == 3
assert sol.longestCommonSubsequence("abc", "abc") == 3
assert sol.longestCommonSubsequence("abc", "def") == 0

assert Solution().longestCommonSubsequence("", "") == 0
assert Solution().longestCommonSubsequence("a", "") == 0
assert Solution().longestCommonSubsequence("", "a") == 0
assert Solution().longestCommonSubsequence("a", "a") == 1
assert Solution().longestCommonSubsequence("aaaaa", "aaa") == 3
assert Solution().longestCommonSubsequence("abcabcabc", "abc") == 3
assert Solution().longestCommonSubsequence("xyz", "xyzxyzxyz") == 3
