"""
URL: https://leetcode.com/problems/percentage-of-letter-in-string/description/?envType=problem-list-v2&envId=vn57k9wr

2278. Percentage of Letter in String

Given a string s and a character letter, return the percentage of characters in s that equal letter rounded down to the nearest whole percent.


Example 1:

Input: s = "foobar", letter = "o"
Output: 33
Explanation:
The percentage of characters in s that equal the letter 'o' is 2 / 6 * 100% = 33% when rounded down, so we return 33.

Example 2:

Input: s = "jjjj", letter = "k"
Output: 0
Explanation:
The percentage of characters in s that equal the letter 'k' is 0%, so we return 0.


Constraints:

    1 <= s.length <= 100
    s consists of lowercase English letters.
    letter is a lowercase English letter.
"""


class Solution:
    def percentageLetter(self, s: str, letter: str) -> int:
        n = len(s)
        count = s.count(letter)
        return int((count / n) * 100)


sol = Solution()

# print(sol.percentageLetter("foobar", "o"))  # 33

assert sol.percentageLetter("foobar", "o") == 33
assert sol.percentageLetter("jjjj", "k") == 0
assert sol.percentageLetter("a", "a") == 100
assert sol.percentageLetter("a", "b") == 0
assert sol.percentageLetter("abc", "a") == 33
assert sol.percentageLetter("aaaa", "a") == 100
assert sol.percentageLetter("abcd", "e") == 0
assert sol.percentageLetter("aaabbbb", "a") == 42
assert sol.percentageLetter("abcd", "a") == 25
assert sol.percentageLetter("a" + "b" * 98, "a") == 1
