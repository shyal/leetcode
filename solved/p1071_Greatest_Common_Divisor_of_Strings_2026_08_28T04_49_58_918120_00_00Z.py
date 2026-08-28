"""
URL: https://leetcode.com/problems/greatest-common-divisor-of-strings/description/?envType=problem-list-v2&envId=vn57k9wr

1071. Greatest Common Divisor of Strings

For two strings s and t, we say "t divides s" if and only if
s = t + t + t + ... + t + t (i.e., t is concatenated with itself one or more times).

Given two strings str1 and str2, return the largest string x such that x divides
both str1 and str2.


Example 1:

Input: str1 = "ABCABC", str2 = "ABC"
Output: "ABC"

Example 2:

Input: str1 = "ABABAB", str2 = "ABAB"
Output: "AB"

Example 3:

Input: str1 = "LEET", str2 = "CODE"
Output: ""

Example 4:

Input: str1 = "AAAAAB", str2 = "AAA"
Output: ""


Constraints:

    1 <= str1.length, str2.length <= 1000
    str1 and str2 consist of English uppercase letters.
"""


class Solution:
    def gcdOfStrings(self, str1: str, str2: str) -> str:
        def divides(a, b):
            return not any(b.split(a))

        long, short = (str1, str2) if len(str1) > len(str2) else (str2, str1)
        for i in range(len(short)):
            st = short[: len(short) - i]
            if divides(st, short) and divides(st, long):
                return st
        return ""


sol = Solution()

print(sol.gcdOfStrings("AAA", "AA"))

print(sol.gcdOfStrings("ABCABC", "ABC"))  # "ABC"

assert sol.gcdOfStrings("ABCABC", "ABC") == "ABC"
assert sol.gcdOfStrings("ABABAB", "ABAB") == "AB"
assert sol.gcdOfStrings("LEET", "CODE") == ""
assert sol.gcdOfStrings("AAAAAB", "AAA") == ""

assert sol.gcdOfStrings("A", "A") == "A"
assert sol.gcdOfStrings("A", "B") == ""
assert sol.gcdOfStrings("AB", "AB") == "AB"
assert sol.gcdOfStrings("ABCDEFGHIJ", "ABCDEFGHIJ") == "ABCDEFGHIJ"

assert sol.gcdOfStrings("ABC", "ABCABC") == "ABC"
assert sol.gcdOfStrings("ABAB", "ABABAB") == "AB"
assert sol.gcdOfStrings("AB", "ABAB") == "AB"
assert sol.gcdOfStrings("ABABABAB", "ABAB") == "ABAB"
assert sol.gcdOfStrings("ABABABAB", "ABABAB") == "AB"
assert sol.gcdOfStrings("XYZXYZXYZ", "XYZXYZ") == "XYZ"
assert sol.gcdOfStrings("ABCABCABC", "ABCABC") == "ABC"

assert sol.gcdOfStrings("AAAAAA", "AA") == "AA"
assert sol.gcdOfStrings("AAAAAA", "AAA") == "AAA"
assert sol.gcdOfStrings("AAA", "AA") == "A"
assert sol.gcdOfStrings("AAAA", "AA") == "AA"
assert sol.gcdOfStrings("AAAAA", "AAA") == "A"

assert sol.gcdOfStrings("ABC", "BCA") == ""
assert sol.gcdOfStrings("AAB", "ABA") == ""
assert sol.gcdOfStrings("ABCDEF", "ABC") == ""
assert sol.gcdOfStrings("ABC", "ABCD") == ""
assert sol.gcdOfStrings("ABAB", "ABA") == ""
assert sol.gcdOfStrings("AB", "A") == ""
assert sol.gcdOfStrings("A", "AB") == ""
assert sol.gcdOfStrings("ABCABCAB", "ABC") == ""
assert sol.gcdOfStrings("ABABABA", "ABAB") == ""

assert sol.gcdOfStrings("A" * 1000, "A" * 999) == "A"
assert sol.gcdOfStrings("A" * 1000, "A" * 500) == "A" * 500
assert sol.gcdOfStrings("AB" * 500, "AB" * 250) == "AB" * 250
assert sol.gcdOfStrings("AB" * 500, "AB" * 333) == "AB"
assert sol.gcdOfStrings("AB" * 499 + "AC", "AB" * 250) == ""
assert sol.gcdOfStrings("ABC" * 333, "ABC" * 111) == "ABC" * 111
