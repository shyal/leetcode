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

LEETCODE: Accepted (0 ms, 19.2 MB)
"""


class Solution:
    def freqAlphabets(self, s: str) -> str:
        for i in range(10, 27):
            s = s.replace(f"{i}#", chr(ord("j") + i - 10))
        for i in range(1, 10):
            s = s.replace(f"{i}", chr(ord("a") + i - 1))
        return s


sol = Solution()

print(sol.freqAlphabets("10#11#12"))  # "jkab"

assert sol.freqAlphabets("10#11#12") == "jkab"
assert sol.freqAlphabets("1326#") == "acz"

assert sol.freqAlphabets("1") == "a"
assert sol.freqAlphabets("9") == "i"
assert sol.freqAlphabets("10#") == "j"
assert sol.freqAlphabets("26#") == "z"
assert sol.freqAlphabets("123456789") == "abcdefghi"
assert (
    sol.freqAlphabets("10#11#12#13#14#15#16#17#18#19#20#21#22#23#24#25#26#")
    == "jklmnopqrstuvwxyz"
)
assert sol.freqAlphabets("1111111111") == "aaaaaaaaaa"
assert sol.freqAlphabets("10#10#10#10#") == "jjjj"
assert sol.freqAlphabets("26#26#26#26#") == "zzzz"
assert (
    sol.freqAlphabets("10#" * 333 + "1")
    == "jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjja"
)
