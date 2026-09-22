# combo chain: two-sequence-align, problem 6 of 14. Run `make combos two-sequence-align` to see
# the chain and what is done today; the chain is saved in graph/chains/two-sequence-align.json.
"""
URL: https://leetcode.com/problems/shortest-common-supersequence/description/?envType=problem-list-v2&envId=vn57k9wr

1092. Shortest Common Supersequence

Given two strings str1 and str2, return the shortest string that has both str1 and str2 as subsequences. If there are multiple valid strings, return any of them.

A string s is a subsequence of string t if deleting some number of characters from t (possibly 0) results in the string s.

Example 1:

Input: str1 = "abac", str2 = "cab"
Output: "cabac"
Explanation:
str1 = "abac" is a subsequence of "cabac" because we can delete the first "c".
str2 = "cab" is a subsequence of "cabac" because we can delete the last "ac".
The answer provided is the shortest such string that satisfies these properties.

Example 2:

Input: str1 = "aaaaaaaa", str2 = "aaaaaaaa"
Output: "aaaaaaaa"

Constraints:

    1 <= str1.length, str2.length <= 1000
    str1 and str2 consist of lowercase English letters.

---

Learning

LEETCODE: Memory Limit Exceeded (50/50 cases)
"""


class Solution:
    def shortestCommonSupersequence(self, a: str, b: str) -> str:
        a, b = f" {a}", f" {b}"
        dp = table(len(a), len(b), fill="")
        for i in range(len(a)):
            dp[i][0] = a[1 : i + 1]
        for j in range(len(b)):
            dp[0][j] = b[1 : j + 1]
        # tabulate(dp, headers=list(b), row_labels=list(a))
        for i, j in cells(dp, start=1):
            # tabulate(dp, headers=list(b), row_labels=list(a))
            if a[i] == b[j]:
                dp[i][j] = dp[i - 1][j - 1] + a[i]
            else:
                dp[i][j] = min(dp[i - 1][j] + a[i], dp[i][j - 1] + b[j], key=len)
            # tabulate(dp, headers=list(b), row_labels=list(a))
        # tabulate(dp, headers=list(b), row_labels=list(a))
        return dp[-1][-1]


sol = Solution()

print(sol.shortestCommonSupersequence("abac", "cab"))  # "cabac"

assert sol.shortestCommonSupersequence("abac", "cab") == "cabac"
assert sol.shortestCommonSupersequence("aaaaaaaa", "aaaaaaaa") == "aaaaaaaa"

assert sol.shortestCommonSupersequence("", "") == ""
assert sol.shortestCommonSupersequence("a", "") == "a"
assert sol.shortestCommonSupersequence("", "a") == "a"
assert sol.shortestCommonSupersequence("abc", "abc") == "abc"
assert sol.shortestCommonSupersequence("abc", "def") == "defabc"
assert sol.shortestCommonSupersequence("aaaaa", "aaa") == "aaaaa"
assert sol.shortestCommonSupersequence("abcde", "ace") == "abcde"
assert sol.shortestCommonSupersequence("ace", "abcde") == "abcde"
assert sol.shortestCommonSupersequence("xyz", "xyzxyzxyz") == "xyzxyzxyz"
