"""
URL: https://leetcode.com/problems/make-the-string-great/description/?envType=problem-list-v2&envId=vn57k9wr

1544. Make The String Great

Given a string s of lower and upper case English letters.

A good string is a string which doesn't have two adjacent characters s[i] and s[i + 1] where:

- 0 <= i <= s.length - 2

- s[i] is a lower-case letter and s[i + 1] is the same letter but in upper-case or vice-versa.

To make the string good, you can choose two adjacent characters that make the string bad and remove them. You can keep doing this until the string becomes good.

Return the string after making it good. The answer is guaranteed to be unique under the given constraints.

Notice that an empty string is also good.

Example 1:

Input: s = "leEeetcode"
Output: "leetcode"
Explanation: In the first step, either you choose i = 1 or i = 2, both will result "leEeetcode" to be reduced to "leetcode".

Example 2:

Input: s = "abBAcC"
Output: ""
Explanation: We have many possible scenarios, and all lead to the same answer. For example:
"abBAcC" --> "aAcC" --> "cC" --> ""
"abBAcC" --> "abBA" --> "aA" --> ""

Example 3:

Input: s = "s"
Output: "s"

Constraints:

- 1 <= s.length <= 100
- s contains only lower and upper case English letters.
"""


class Solution:

    def equiv(self, a, b):
        return a != b and a.lower() == b.lower()

    def makesGood(self, s):
        for i in range(1, len(s)):
            if self.equiv(s[i - 1], s[i]):
                return s[: i - 1] + s[i + 1 :]
        return s

    def makeGood(self, s: str) -> str:
        prev = None
        while s != prev:
            prev = s
            s = self.makesGood(s)
        return s


sol = Solution()

# print(sol.makeGood("leEeetcode"))  # "leetcode"

assert sol.makeGood("leEeetcode") == "leetcode"
assert sol.makeGood("abBAcC") == ""
assert sol.makeGood("s") == "s"
assert sol.makeGood("Aa") == ""
assert sol.makeGood("aA") == ""
assert sol.makeGood("aa") == "aa"
assert sol.makeGood("Ab") == "Ab"
assert sol.makeGood("abAB") == "abAB"
assert sol.makeGood("aAa") == "a"
assert sol.makeGood("aaA") == "a"
assert sol.makeGood("AaAa") == ""
assert sol.makeGood("AaAaA") == "A"
assert sol.makeGood("abcDEF") == "abcDEF"
assert sol.makeGood("Ppq") == "q"
assert sol.makeGood("qPp") == "q"
assert sol.makeGood("AAAA") == "AAAA"
assert sol.makeGood("aaaa") == "aaaa"
assert sol.makeGood("aBcD") == "aBcD"
