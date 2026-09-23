# combo chain: two-sequence-align, problem 10 of 14. Run `make combos two-sequence-align` to see
# the chain and what is done today; the chain is saved in graph/chains/two-sequence-align.json.
"""
URL: https://leetcode.com/problems/distinct-subsequences/description/?envType=problem-list-v2&envId=vn57k9wr

115. Distinct Subsequences

Given two strings s and t, return the number of distinct subsequences of s which equals t.

The test cases are generated so that the answer fits on a 32-bit signed integer.

Example 1:

Input: s = "rabbbit", t = "rabbit"
Output: 3
Explanation:
As shown below, there are 3 ways you can generate "rabbit" from s.
rabbbit
rabbbit
rabbbit

Example 2:

Input: s = "babgbag", t = "bag"
Output: 5
Explanation:
As shown below, there are 5 ways you can generate "bag" from s.
babgbag
babgbag
babgbag
babgbag
babgbag

Constraints:

    1 <= s.length, t.length <= 1000
    s and t consist of English letters.

---

Out of my depth. Built some drills and gating.

Learning.

LEETCODE: Accepted (527 ms, 75.7 MB)
"""


class Solution:
    def numDistinct(self, s: str, t: str) -> int:
        s, t = f" {s}", f" {t}"
        dp = table(len(s), len(t))
        for i in range(len(s)):
            dp[i][0] = 1
        for i, j in cells(dp, start=1):
            dp[i][j] = dp[i - 1][j]
            if s[i] == t[j]:
                dp[i][j] += dp[i - 1][j - 1]
        # tabulate(dp, headers=list(t), row_labels=list(s))
        return dp[-1][-1]


sol = Solution()

print(sol.numDistinct("rabbbit", "rabbit"))  # 3

assert sol.numDistinct("rabbbit", "rabbit") == 3
assert sol.numDistinct("babgbag", "bag") == 5

assert sol.numDistinct("", "") == 1
assert sol.numDistinct("a", "") == 1
assert sol.numDistinct("", "a") == 0
assert sol.numDistinct("a", "a") == 1
assert sol.numDistinct("aaaaa", "aa") == 10
assert sol.numDistinct("abcde", "ace") == 1
assert sol.numDistinct("abcde", "aec") == 0
assert sol.numDistinct("a" * 1000, "a" * 1000) == 1
assert sol.numDistinct("a" * 1000, "b" * 1000) == 0
assert sol.numDistinct("abcabcabc", "abc") == 10
assert sol.numDistinct("abcabcabc", "aaa") == 1
assert sol.numDistinct("xyz" * 333 + "x", "xyzxyzxyzxyz") == 4243238407510714696370
