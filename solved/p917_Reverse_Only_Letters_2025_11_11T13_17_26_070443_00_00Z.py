"""
URL: https://leetcode.com/problems/reverse-only-letters/description/?envType=problem-list-v2&envId=vn57k9wr

917. Reverse Only Letters

Given a string s, reverse the string according to the following rules:

- All the characters that are not English letters remain in the same position.
- All the English letters (lowercase or uppercase) should be reversed.

Return s after reversing it.

Example 1:

Input: s = "ab-cd"
Output: "dc-ba"

Example 2:

Input: s = "a-bC-dEf-ghIj"
Output: "j-Ih-gfE-dCba"

Example 3:

Input: s = "Test1ng-Leet=code-Q!"
Output: "Qedo1ct-eeLg=ntse-T!"

Constraints:

- 1 <= s.length <= 100
- s consists of characters with ASCII values in the range [33, 122].
- s does not contain '\"' or '\\'.
"""


class Solution:
    def reverseOnlyLetters(self, s: str) -> str:
        s = list(s)
        english = set(ascii_letters)
        to_move = []
        for c in s:
            if c in english:
                to_move.append(c)
        to_move = to_move[::-1]
        for i in reversed(range(len(s))):
            if s[i] in english:
                s[i] = to_move.pop()
        return "".join(s)


sol = Solution()

# print(sol.reverseOnlyLetters("ab-cd"))  # "dc-ba"

assert sol.reverseOnlyLetters("ab-cd") == "dc-ba"
assert sol.reverseOnlyLetters("a-bC-dEf-ghIj") == "j-Ih-gfE-dCba"
assert sol.reverseOnlyLetters("Test1ng-Leet=code-Q!") == "Qedo1ct-eeLg=ntse-T!"
assert sol.reverseOnlyLetters("7_28]") == "7_28]"
assert sol.reverseOnlyLetters("abc") == "cba"
assert sol.reverseOnlyLetters("ABC") == "CBA"
assert sol.reverseOnlyLetters("a") == "a"
assert sol.reverseOnlyLetters("!") == "!"
assert sol.reverseOnlyLetters("-a-") == "-a-"
assert sol.reverseOnlyLetters("a!!b") == "b!!a"
assert sol.reverseOnlyLetters("ab-c") == "cb-a"
assert sol.reverseOnlyLetters("a1b2c") == "c1b2a"
assert sol.reverseOnlyLetters("Ab-C") == "Cb-A"
assert sol.reverseOnlyLetters("aaa") == "aaa"
assert sol.reverseOnlyLetters("z-a") == "a-z"
