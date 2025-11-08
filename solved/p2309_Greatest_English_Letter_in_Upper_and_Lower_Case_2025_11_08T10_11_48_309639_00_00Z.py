"""
URL: https://leetcode.com/problems/greatest-english-letter-in-upper-and-lower-case/description/?envType=problem-list-v2&envId=vn57k9wr

2309. Greatest English Letter in Upper and Lower Case

Given a string of English letters s, return the greatest English letter which occurs as both a lowercase and uppercase letter in s. The returned letter should be in uppercase. If no such letter exists, return an empty string.

An English letter b is greater than another letter a if b appears after a in the English alphabet.

Example 1:

Input: s = "lEeTcOdE"
Output: "E"
Explanation:
The letter 'E' is the only letter to appear in both lower and upper case.

Example 2:

Input: s = "arRAzFif"
Output: "R"
Explanation:
The letter 'R' is the greatest letter to appear in both lower and upper case.
Note that 'A' and 'F' also appear in both lower and upper case, but 'R' is greater than 'F' or 'A'.

Example 3:

Input: s = "AbCdEfGhIjK"
Output: ""
Explanation:
There is no letter that appears in both lower and upper case.

Constraints:

    1 <= s.length <= 1000
    s consists of lowercase and uppercase English letters.
"""


class Solution:
    def greatestLetter(self, s: str) -> str:
        low = set(ascii_lowercase)
        upp = set(ascii_uppercase)
        low = set(x for x in s if x in low)
        return next(
            (
                u
                for u in sorted((x for x in s if x in upp), reverse=True)
                if u.lower() in low
            ),
            "",
        )


sol = Solution()

# print(sol.greatestLetter("lEeTcOdE"))  # "E"

assert sol.greatestLetter("lEeTcOdE") == "E"
assert sol.greatestLetter("arRAzFif") == "R"
assert sol.greatestLetter("AbCdEfGhIjK") == ""

assert sol.greatestLetter("aA") == "A"
assert sol.greatestLetter("zZ") == "Z"
assert sol.greatestLetter("abc") == ""
assert sol.greatestLetter("ABC") == ""
assert sol.greatestLetter("AaBbCc") == "C"
assert sol.greatestLetter("ZzYyXx") == "Z"
assert sol.greatestLetter("A") == ""
assert sol.greatestLetter("a") == ""
assert sol.greatestLetter("AbCa") == "A"
assert sol.greatestLetter("cCaAbB") == "C"
assert sol.greatestLetter("AaZz") == "Z"
assert sol.greatestLetter("xyzXYZ") == "Z"
assert sol.greatestLetter("AaAaaa") == "A"
