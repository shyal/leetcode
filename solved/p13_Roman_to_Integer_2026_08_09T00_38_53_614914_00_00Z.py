"""
URL: https://leetcode.com/problems/roman-to-integer/description/?envType=problem-list-v2&envId=vn57k9wr

13. Roman to Integer

Roman numerals are represented by seven different symbols: I, V, X, L, C, D and M.

Symbol       Value
I             1
V             5
X             10
L             50
C             100
D             500
M             1000

For example, 2 is written as II in Roman numeral, just two ones added together.
12 is written as XII, which is simply X + II. The number 27 is written as XXVII,
which is XX + V + II.

Roman numerals are usually written largest to smallest from left to right.
However, the numeral for four is not IIII. Instead, the number four is written
as IV. Because the one is before the five we subtract it making four. The same
principle applies to the number nine, which is written as IX. There are six
instances where subtraction is used:

    - I can be placed before V (5) and X (10) to make 4 and 9.
    - X can be placed before L (50) and C (100) to make 40 and 90.
    - C can be placed before D (500) and M (1000) to make 400 and 900.

Given a roman numeral, convert it to an integer.


Example 1:

Input: s = "III"
Output: 3
Explanation: III = 3.

Example 2:

Input: s = "LVIII"
Output: 58
Explanation: L = 50, V= 5, III = 3.

Example 3:

Input: s = "MCMXCIV"
Output: 1994
Explanation: M = 1000, CM = 900, XC = 90 and IV = 4.


Constraints:

    1 <= s.length <= 15
    s contains only the characters ('I', 'V', 'X', 'L', 'C', 'D', 'M').
    It is guaranteed that s is a valid roman numeral in the range [1, 3999].
"""

D = {
    'I': 1,
    'V': 5,
    'X': 10,
    'L': 50,
    'C': 100,
    'D': 500,
    'M': 1000
}

class Solution:
    def romanToInt(self, s: str) -> int:
        def func(acc, i):
            return acc + (-D[s[i]] if i < len(s) -1 and ((s[i] == 'I' and s[i+1] in 'VX') or (s[i] == 'X' and s[i+1] in 'LC') or (s[i] == 'C' and s[i+1] in 'DM')) else D[s[i]])
        return reduce(func, range(len(s)), 0)


sol = Solution()

assert sol.romanToInt("III") == 3
assert sol.romanToInt("LVIII") == 58
assert sol.romanToInt("MCMXCIV") == 1994
assert sol.romanToInt("I") == 1
assert sol.romanToInt("V") == 5
assert sol.romanToInt("X") == 10
assert sol.romanToInt("L") == 50
assert sol.romanToInt("C") == 100
assert sol.romanToInt("D") == 500
assert sol.romanToInt("M") == 1000
assert sol.romanToInt("IV") == 4
assert sol.romanToInt("IX") == 9
assert sol.romanToInt("XL") == 40
assert sol.romanToInt("XC") == 90
assert sol.romanToInt("CD") == 400
assert sol.romanToInt("CM") == 900
assert sol.romanToInt("XIV") == 14
assert sol.romanToInt("XXVII") == 27
assert sol.romanToInt("LXXXIX") == 89
assert sol.romanToInt("CDXLIV") == 444
assert sol.romanToInt("CMXCIX") == 999
assert sol.romanToInt("MDCLXVI") == 1666
assert sol.romanToInt("MMM") == 3000
assert sol.romanToInt("MMMCMXCIX") == 3999
assert sol.romanToInt("MMXXVI") == 2026
assert sol.romanToInt("DCXXI") == 621