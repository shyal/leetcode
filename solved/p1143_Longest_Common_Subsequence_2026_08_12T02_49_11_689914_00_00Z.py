"""
URL: https://leetcode.com/problems/longest-common-subsequence/description/?envType=problem-list-v2&envId=vn57k9wr

1143. Longest Common Subsequence

Given two strings text1 and text2, return the length of their longest common
subsequence. If there is no common subsequence, return 0.

A subsequence of a string is a new string generated from the original string
with some characters (can be none) deleted without changing the relative order
of the remaining characters.

    - For example, "ace" is a subsequence of "abcde".

A common subsequence of two strings is a subsequence that is common to both
strings.


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

I was able to port the delete distance (which i just solved with a peek).

Then i had to get hinted to drop the substitution branch, as well as the final
(len(a) + len(b) - dd) // 2 solution.

Also the string version of DP exceeds memory limit on leetcode. So i pretty much
copied the index based solution from edit distance, and removed the sub branch.
"""


class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:

        @cache
        def dp(i, j):
            if i < 0:
                return j + 1
            if j < 0:
                return i + 1
            if text1[i] == text2[j]:
                return dp(i - 1, j - 1)
            add = dp(i, j - 1)
            rem = dp(i - 1, j)
            return min(add, rem) + 1

        dd = dp(len(text1)-1, len(text2)-1)
        chars = len(text1) + len(text2)
        return (chars -dd) // 2



sol = Solution()

assert sol.longestCommonSubsequence("abcde", "ace") == 3
assert sol.longestCommonSubsequence("abc", "abc") == 3
assert sol.longestCommonSubsequence("abc", "def") == 0
assert sol.longestCommonSubsequence("a", "a") == 1
assert sol.longestCommonSubsequence("a", "b") == 0
assert sol.longestCommonSubsequence("a", "abc") == 1
assert sol.longestCommonSubsequence("abc", "a") == 1
assert sol.longestCommonSubsequence("aaaa", "aa") == 2
assert sol.longestCommonSubsequence("aaaa", "aaaa") == 4
assert sol.longestCommonSubsequence("abcdef", "fedcba") == 1
assert sol.longestCommonSubsequence("abcdgh", "aedfhr") == 3
assert sol.longestCommonSubsequence("abcba", "abcbcba") == 5
assert sol.longestCommonSubsequence("bbbab", "babbb") == 4
assert sol.longestCommonSubsequence("ezupkr", "ubmrapg") == 2
assert sol.longestCommonSubsequence("bl", "yby") == 1
assert sol.longestCommonSubsequence("xyz", "xz") == 2
