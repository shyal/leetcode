"""
URL: https://leetcode.com/problems/decrypt-string-from-alphabet-to-integer-mapping/description/?envType=problem-list-v2&envId=vn57k9wr

1309. Decrypt String from Alphabet to Integer Mapping

You are given a string s formed by digits and '#'. We want to map s to English lowercase characters as follows:

- Characters ('a' to 'i') are represented by ('1' to '9') respectively.
- Characters ('j' to 'z') are represented by ('10#' to '26#') respectively.

Return the string formed after mapping.

The test cases are generated so that a unique mapping will always exist.

Example 1:

Input: s = "10#11#12"
Output: "jkab"
Explanation: "j" -> "10#" , "k" -> "11#" , "a" -> "1" , "b" -> "2".

Example 2:

Input: s = "1326#"
Output: "acz"

Constraints:

    1 <= s.length <= 1000
    s consists of digits and the '#' letter.
    s will be a valid string such that mapping is always possible.

---

LEETCODE: Accepted (1 ms, 19.3 MB)
"""


# mu 0.12
# class Solution
#   def freqAlphabets(s: str) -> str
#     res = []
#     skip = 0
#     for <i, c in s
#       if skip
#         skip -= 1
#         continue
#       if '1' <= c <= '9'
#         res <- chr(ord('a') + int(c)-1)
#       elif c == '#'
#         num = s[i-2:i]
#         res <- chr(ord('a') + int(num) - 1)
#         skip = 2
#     ''.join(res[::-1])
#

class Solution:
    def freqAlphabets(self, s: str) -> str:
        res = []
        skip = 0
        for i, c in zip(range(len(s) - 1, -1, -1), reversed(s)):
            if skip:
                skip -= 1
                continue
            if '1' <= c <= '9':
                res.append(chr(ord('a') + int(c) - 1))
            elif c == '#':
                num = s[i - 2:i]
                res.append(chr(ord('a') + int(num) - 1))
                skip = 2
        return ''.join(res[::-1])


sol = Solution()
print(sol.freqAlphabets('10#11#12'))
_l, _r = sol.freqAlphabets('10#11#12'), 'jkab'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.freqAlphabets('1326#'), 'acz'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.freqAlphabets('1'), 'a'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.freqAlphabets('9'), 'i'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.freqAlphabets('10#'), 'j'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.freqAlphabets('26#'), 'z'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.freqAlphabets('123456789'), 'abcdefghi'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.freqAlphabets('10#11#12#13#14#15#16#17#18#19#20#21#22#23#24#25#26#'), 'jklmnopqrstuvwxyz'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.freqAlphabets('1111111111'), 'aaaaaaaaaa'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.freqAlphabets('10#10#10#10#'), 'jjjj'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.freqAlphabets('26#26#26#26#'), 'zzzz'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.freqAlphabets('10#' * 333 + '1'), 'jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjja'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
