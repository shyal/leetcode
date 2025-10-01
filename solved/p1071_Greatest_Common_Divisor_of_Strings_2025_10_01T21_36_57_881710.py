"""
https://leetcode.com/problems/greatest-common-divisor-of-strings/description

1071. Greatest Common Divisor of Strings
Easy
For two strings s and t, we say "t divides s" if and only if s = t + t + t + ... + t + t (i.e., t is concatenated with itself one or more times).

Given two strings str1 and str2, return the largest string x such that x divides both str1 and str2.

Example 1:

Input: str1 = "ABCABC", str2 = "ABC"
Output: "ABC"
Example 2:

Input: str1 = "ABABAB", str2 = "ABAB"
Output: "AB"
Example 3:

Input: str1 = "LEET", str2 = "CODE"
Output: ""

Constraints:

1 <= str1.length, str2.length <= 1000
str1 and str2 consist of English uppercase letters.

"""

from itertools import zip_longest


class Solution:
    def gcdOfStrings(self, str1: str, str2: str) -> str:
        def batched(s, n=1):
            r = list(range(0, len(s), n))
            return [s[a:b] for a, b in zip_longest(r, r[1:])]

        batch_match = lambda x: all([a == b for a, b in zip(x, x[1:])])

        for n in range(len(str2), 0, -1):
            b1, b2 = batched(str1, n), batched(str2, n)
            if b1[0] == b2[0] and batch_match(b1) and batch_match(b2):
                return b1[0]

        return ""


sol = Solution()

assert sol.gcdOfStrings(str1="ABCABC", str2="ABC") == "ABC"
assert sol.gcdOfStrings(str1="ABABAB", str2="ABAB") == "AB"
assert sol.gcdOfStrings(str1="LEET", str2="CODE") == ""
assert sol.gcdOfStrings(str1="A", str2="A") == "A"
assert sol.gcdOfStrings(str1="A", str2="B") == ""
assert sol.gcdOfStrings(str1="A", str2="AAA") == "A"
assert sol.gcdOfStrings(str1="AAAA", str2="AA") == "AA"
assert sol.gcdOfStrings(str1="AAA", str2="AA") == "A"
assert sol.gcdOfStrings(str1="ABCDEF", str2="ABC") == ""
assert sol.gcdOfStrings(str1="ABC", str2="ABC") == "ABC"
assert sol.gcdOfStrings(str1="AB", str2="ABABAB") == "AB"
assert sol.gcdOfStrings(str1="ABAB", str2="BABA") == ""
assert sol.gcdOfStrings(str1="ABCABCABCABC", str2="ABCABCABC") == "ABC"

