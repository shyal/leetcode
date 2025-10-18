"""
URL: https://leetcode.com/problems/decrypt-string-from-alphabet-to-integer-mapping/description/?envType=problem-list-v2&envId=vn57k9wr

1309. Decrypt String from Alphabet to Integer Mapping

You are given a string s formed by digits and '#'. We want to map s to English lowercase characters as follows:

        Characters ('a' to 'i') are represented by ('1' to '9') respectively.
        Characters ('j' to 'z') are represented by ('10#' to '26#') respectively.

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

Not my solution. I didn't think of using a stack.

Revisit.

"""


class Solution:
    def freqAlphabets(self, s: str) -> str:
        s, res = list(s), ""
        while s:
            c = s.pop()
            if c == "#":
                x = s.pop() + s.pop()
                res += chr(ord("a") + int(x[::-1]) - 1)
            else:
                res += chr(ord("a") + int(c) - 1)
        return res[::-1]


sol = Solution()
res = sol.freqAlphabets(s="10#11#12")
# print(res)
assert res == "jkab"
