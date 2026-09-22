"""
URL: https://leetcode.com/problems/minimum-ascii-delete-sum-for-two-strings/description/?envType=problem-list-v2&envId=vn57k9wr

712. Minimum ASCII Delete Sum for Two Strings

Given two strings s1 and s2, return the lowest ASCII sum of deleted characters to make two strings equal.

Example 1:

Input: s1 = "sea", s2 = "eat"
Output: 231
Explanation: Deleting "s" from "sea" adds the ASCII value of "s" (115) to the sum.
Deleting "t" from "eat" adds 116 to the sum.
At the end, both strings are equal, and 115 + 116 = 231 is the minimum sum possible to achieve this.

Example 2:

Input: s1 = "delete", s2 = "leet"
Output: 403
Explanation: Deleting "dee" from "delete" to turn the string into "let",
adds 100[d] + 101[e] + 101[e] to the sum.
Deleting "e" from "leet" adds 101[e] to the sum.
At the end, both strings are equal to "let", and the answer is 100+101+101+101 = 403.
If instead we turned both strings into "lee" or "eet", we would get answers of 433 or 417, which are higher.

Constraints:

    1 <= s1.length, s2.length <= 1000
    s1 and s2 consist of lowercase English letters.

---

LEETCODE: Accepted (1191 ms, 480.9 MB)
"""


class Solution:
    def minimumDeleteSum(self, s1: str, s2: str) -> int:
        asum = lambda x: sum(ord(y) for y in x)

        @cache
        def helper(a, b):
            if len(a) == 0 or len(b) == 0:
                return asum(a or b)
            if a[-1] == b[-1]:
                return helper(a[:-1], b[:-1])
            dela = helper(a[:-1], b) + ord(a[-1])
            delb = helper(a, b[:-1]) + ord(b[-1])
            return min(dela, delb)

        return helper(s1, s2)


sol = Solution()

print(sol.minimumDeleteSum("sea", "eat"))  # 231

assert sol.minimumDeleteSum("sea", "eat") == 231
assert sol.minimumDeleteSum("delete", "leet") == 403

assert sol.minimumDeleteSum("", "") == 0
assert sol.minimumDeleteSum("a", "") == 97
assert sol.minimumDeleteSum("", "a") == 97
assert sol.minimumDeleteSum("a", "a") == 0
assert sol.minimumDeleteSum("abc", "abc") == 0
assert sol.minimumDeleteSum("abc", "def") == 597
assert sol.minimumDeleteSum("aaaaa", "aaa") == 194
assert sol.minimumDeleteSum("abcde", "ace") == 198
assert sol.minimumDeleteSum("abc", "cba") == 390
# assert sol.minimumDeleteSum("z" * 1000, "z" * 1000) == 0
# assert sol.minimumDeleteSum("a" * 1000, "b" * 1000) == 195000
assert (
    sol.minimumDeleteSum("abcdefghijklmnopqrstuvwxyz", "zyxwvutsrqponmlkjihgfedcba")
    == 5450
)
