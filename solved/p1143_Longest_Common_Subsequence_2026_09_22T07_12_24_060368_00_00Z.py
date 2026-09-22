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

LEETCODE: Accepted (390 ms, 44.5 MB)
"""


class Solution:
    def longestCommonSubsequence(self, a: str, b: str) -> int:
        a = f" {a}"
        b = f" {b}"
        dp = table(len(a), len(b))
        for i, j in cells(dp, start=1):
            if a[i] == b[j]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i][j - 1], dp[i - 1][j])
        return dp[-1][-1]


sol = Solution()

print(sol.longestCommonSubsequence("abcde", "ace"))  # 3

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
assert Solution().longestCommonSubsequence("psnw", "vozsh") == 1
