"""
345. Reverse Vowels of a String
Easy
Given a string s, reverse only all the vowels in the string and return it.

The vowels are 'a', 'e', 'i', 'o', and 'u', and they can appear in both lower and upper cases, more than once.

Example 1:

Input: s = "IceCreAm"

Output: "AceCreIm"

Explanation:

The vowels in s are ['I', 'e', 'e', 'A']. On reversing the vowels, s becomes "AceCreIm".

Example 2:

Input: s = "leetcode"

Output: "leotcede"


Constraints:

1 <= s.length <= 3 * 105
s consist of printable ASCII characters.
"""


class Solution:
    def reverseVowels(self, s: str) -> str:
        s = list(s)
        v = set("aeiouAEIOU")
        left = 0
        right = len(s) - 1
        while left <= right:
            left_is_vowel = s[left] in v
            right_is_vowel = s[right] in v
            if left_is_vowel and right_is_vowel:
                s[left], s[right] = s[right], s[left]
                left += 1
                right -= 1
                continue
            if not left_is_vowel:
                left += 1
            if not right_is_vowel:
                right -= 1
        return "".join(s)


sol = Solution()

assert sol.reverseVowels(s="IceCreAm") == "AceCreIm"
assert sol.reverseVowels(s="") == ""
assert sol.reverseVowels(s="a") == "a"
assert sol.reverseVowels(s="avi") == "iva"
assert sol.reverseVowels(s="aviz") == "ivaz"
assert sol.reverseVowels(s="foobar") == "faobor"
assert sol.reverseVowels(s="leetcode") == "leotcede"
assert sol.reverseVowels(s="hello") == "holle"
assert sol.reverseVowels(s="AEIOU") == "UOIEA"
assert sol.reverseVowels(s="why") == "why"
assert sol.reverseVowels(s="a!e") == "e!a"
assert sol.reverseVowels(s="aaee") == "eeaa"
assert sol.reverseVowels(s="bcdfg") == "bcdfg"
assert sol.reverseVowels(s="b") == "b"
assert sol.reverseVowels(s="123aei456ou789") == "123uoi456ea789"
assert sol.reverseVowels(s="AaEeIiOoUu") == "uUoOiIeEaA"
assert (
    sol.reverseVowels(s="A man a plan a canal: Panama")
    == "a man a plan a canal: PanamA"
)


