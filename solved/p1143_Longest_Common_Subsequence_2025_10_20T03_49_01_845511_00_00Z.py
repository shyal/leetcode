"""
URL: https://leetcode.com/problems/longest-common-subsequence/description/

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
"""


class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        text1 = " " + text1
        text2 = " " + text2
        dp = []
        for _ in range(len(text1)):
            dp.append([0] * len(text2))

        for i in range(len(text1)):
            for j in range(len(text2)):
                if text1[i] == text2[j]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i][j - 1], dp[i - 1][j])

        # tabulate(dp, headers=text2, row_labels=text1)
        return dp[-1][-1] - 1


sol = Solution()

res = sol.longestCommonSubsequence(text1="abcde", text2="ace")

assert sol.longestCommonSubsequence(text1="ab", text2="b") == 1
assert sol.longestCommonSubsequence(text1="abcde", text2="ace") == 3
assert sol.longestCommonSubsequence(text1="abc", text2="abc") == 3
assert sol.longestCommonSubsequence(text1="abc", text2="def") == 0
assert sol.longestCommonSubsequence(text1="psnw", text2="vozsh") == 1
assert sol.longestCommonSubsequence(text1="psnw", text2="vozsh") == 1
