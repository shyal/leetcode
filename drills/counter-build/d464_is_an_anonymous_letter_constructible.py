"""
EPI 12.2 Is an anonymous letter constructible?

Given two strings letter_text and magazine_text, return True when
letter_text can be written with characters cut from magazine_text, and
False otherwise. Each character of magazine_text can be used at most
once. Every character counts, spaces and punctuation too, and case
matters.

Example 1:

Input: letter_text = "pay up", magazine_text = "a yellow pupa"
Output: True
Explanation: the magazine has the letters p, a, y, u, p and a space.

Example 2:

Input: letter_text = "aa", magazine_text = "a"
Output: False
Explanation: the letter needs two "a" and the magazine has only a single "a".

Example 3:

Input: letter_text = "", magazine_text = "abc"
Output: True

Constraints:

    0 <= len(letter_text), len(magazine_text) <= 10^6
    Both strings consist of printable ASCII characters.

    REQUIRED: O(m + n) time, where m and n are the lengths of the two
    strings, and O(L) extra space, where L is the number of distinct
    characters in letter_text.
"""


class Solution:
    def is_letter_constructible_from_magazine(self, letter_text: str, magazine_text: str) -> bool:
        pass


sol = Solution()

print(sol.is_letter_constructible_from_magazine("pay up", "a yellow pupa"))  # True

# assert sol.is_letter_constructible_from_magazine("pay up", "a yellow pupa") is True
# assert sol.is_letter_constructible_from_magazine("aa", "a") is False
# assert sol.is_letter_constructible_from_magazine("", "abc") is True
# assert sol.is_letter_constructible_from_magazine("", "") is True
# assert sol.is_letter_constructible_from_magazine("a", "") is False
# assert sol.is_letter_constructible_from_magazine("a", "a") is True
# assert sol.is_letter_constructible_from_magazine("abc", "cba") is True
# assert sol.is_letter_constructible_from_magazine("Aa", "aa") is False
# assert sol.is_letter_constructible_from_magazine("a b", "ab") is False
# assert sol.is_letter_constructible_from_magazine("hi!", "ih") is False
# assert sol.is_letter_constructible_from_magazine("aab", "baa") is True
# assert sol.is_letter_constructible_from_magazine("ab", "a" * 10 ** 6 + "b") is True
# assert sol.is_letter_constructible_from_magazine("ab", "b" + "a" * 10 ** 6) is True
# assert sol.is_letter_constructible_from_magazine("x" * 10 ** 5, "x" * 10 ** 5) is True
# assert sol.is_letter_constructible_from_magazine("x" * 10 ** 5 + "y", "x" * 10 ** 6) is False
