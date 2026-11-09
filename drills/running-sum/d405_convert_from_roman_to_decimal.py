"""
EPI 6.8 Convert from Roman to decimal

Given a valid Roman number string s, return its value. The symbols are
I = 1, V = 5, X = 10, L = 50, C = 100, D = 500 and M = 1000. In a valid
string the symbols are in nonincreasing order of value, with three
exceptions: I may come directly before V or X, X directly before L or
C, and C directly before D or M. Such a pair has the value of the
larger symbol minus the smaller. Two exception pairs never overlap, so
"IXC" is not valid. A symbol may repeat any number of times.

Example 1:

Input: s = "LIX"
Output: 59
Explanation: L is 50 and the pair IX is 9.

Example 2:

Input: s = "MCMXCIV"
Output: 1994
Explanation: M + CM + XC + IV = 1000 + 900 + 90 + 4.

Example 3:

Input: s = "IIII"
Output: 4

Constraints:

    1 <= len(s) <= 10^5
    s is a valid Roman number string.

    REQUIRED: O(n) time, O(1) extra space. NO replace(), NO regex, NO
    slicing.
"""


class Solution:
    def roman_to_integer(self, s: str) -> int:
        pass


sol = Solution()

print(sol.roman_to_integer("LIX"))  # 59

# assert sol.roman_to_integer("LIX") == 59
# assert sol.roman_to_integer("MCMXCIV") == 1994
# assert sol.roman_to_integer("IIII") == 4
# assert sol.roman_to_integer("I") == 1
# assert sol.roman_to_integer("M") == 1000
# assert sol.roman_to_integer("IV") == 4
# assert sol.roman_to_integer("IX") == 9
# assert sol.roman_to_integer("XL") == 40
# assert sol.roman_to_integer("XC") == 90
# assert sol.roman_to_integer("CD") == 400
# assert sol.roman_to_integer("CM") == 900
# assert sol.roman_to_integer("XIIII") == 14
# assert sol.roman_to_integer("CDXLIV") == 444
# assert sol.roman_to_integer("MMMCMXCIX") == 3999
# assert sol.roman_to_integer("M" * 100000) == 10 ** 8
# assert sol.roman_to_integer("CM" * 50000) == 45000000
# assert sol.roman_to_integer("M" * 99998 + "IV") == 99998004
