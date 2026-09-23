# combo chain: two-sequence-align, problem 12 of 14. Run `make combos two-sequence-align` to see
# the chain and what is done today; the chain is saved in graph/chains/two-sequence-align.json.
"""
URL: https://leetcode.com/problems/interleaving-string/description/?envType=problem-list-v2&envId=vn57k9wr

97. Interleaving String

Given strings s1, s2, and s3, find whether s3 is formed by an interleaving of s1 and s2.

An interleaving of two strings s and t is a configuration where s and t are divided into n and m substrings respectively, such that:

- s = s1 + s2 + ... + sn
- t = t1 + t2 + ... + tm
- |n - m| <= 1
- The interleaving is s1 + t1 + s2 + t2 + s3 + t3 + ... or t1 + s1 + t2 + s2 + t3 + s3 + ...

Note: a + b is the concatenation of strings a and b.

Example 1:

Input: s1 = "aabcc", s2 = "dbbca", s3 = "aadbbcbcac"
Output: true
Explanation: One way to obtain s3 is:
Split s1 into s1 = "aa" + "bc" + "c", and s2 into s2 = "dbbc" + "a".
Interleaving the two splits, we get "aa" + "dbbc" + "bc" + "a" + "c" = "aadbbcbcac".
Since s3 can be obtained by interleaving s1 and s2, we return true.

Example 2:

Input: s1 = "aabcc", s2 = "dbbca", s3 = "aadbbbaccc"
Output: false
Explanation: Notice how it is impossible to interleave s2 with any other string to obtain s3.

Example 3:

Input: s1 = "", s2 = "", s3 = ""
Output: true

Constraints:

    0 <= s1.length, s2.length <= 100
    0 <= s3.length <= 200
    s1, s2, and s3 consist of lowercase English letters.

Follow up: Could you solve it using only O(s2.length) additional memory space?

---

Learning

LEETCODE: Accepted (11 ms, 19.4 MB)
"""


class Solution:
    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
        s1, s2, s3 = f" {s1}", f" {s2}", f" {s3}"
        if len(s1) + len(s2) - 1 != len(s3):
            return False
        dp = table(len(s1), len(s2), fill=False)

        for i, j in cells(dp):
            up = i > 0 and dp[i - 1][j] and s1[i] == s3[i + j]
            left = j > 0 and dp[i][j - 1] and s2[j] == s3[i + j]
            dp[i][j] = (i == j == 0) or up or left
        # tabulate(dp, headers=s2, row_labels=s1)
        return dp[-1][-1]


sol = Solution()

print(sol.isInterleave("aabcc", "dbbca", "aadbbcbcac"))  # True

assert sol.isInterleave("aabcc", "dbbca", "aadbbcbcac") is True
assert sol.isInterleave("aabcc", "dbbca", "aadbbbaccc") is False
assert sol.isInterleave("", "", "") is True

assert sol.isInterleave("", "abc", "abc") == True
assert sol.isInterleave("abc", "", "abc") == True
assert sol.isInterleave("abc", "def", "adbcef") == True
assert sol.isInterleave("abc", "def", "abdecf") == True
assert sol.isInterleave("aaa", "aaa", "aaaaaa") == True
assert sol.isInterleave("aaa", "aaa", "aaaaab") == False
assert sol.isInterleave("a" * 100, "b" * 100, "a" * 100 + "b" * 100) == True
assert sol.isInterleave("a" * 100, "b" * 100, "ab" * 100) == True
assert (
    sol.isInterleave(
        "a" * 50 + "b" * 50, "b" * 50 + "a" * 50, "a" * 50 + "b" * 100 + "a" * 50
    )
    == True
)
assert sol.isInterleave("abc", "def", "abcdefg") == False
assert sol.isInterleave("abc", "def", "abdefc") == True
assert sol.isInterleave("a", "b", "ba") == True
