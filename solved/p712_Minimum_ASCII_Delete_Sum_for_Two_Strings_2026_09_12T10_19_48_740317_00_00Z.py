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
"""


class Solution:
    def minimumDeleteSum(self, s1: str, s2: str) -> int:
        @cache
        def fp(a, b):
            if a == "":
                return sum(ord(x) for x in b)
            if b == "":
                return sum(ord(x) for x in a)

            if a[-1] == b[-1]:
                return fp(a[:-1], b[:-1])

            rema = fp(a[:-1], b) + ord(a[-1])
            remb = fp(a, b[:-1]) + ord(b[-1])

            return min(rema, remb)

        return fp(s1, s2)


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
assert (
    sol.minimumDeleteSum("abcdefghijklmnopqrstuvwxyz", "zyxwvutsrqponmlkjihgfedcba")
    == 5450
)
