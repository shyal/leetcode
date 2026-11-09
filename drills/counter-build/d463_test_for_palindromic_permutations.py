"""
EPI 12.1 Test for palindromic permutations

Given a string s, return True when the characters of s can be reordered
to form a palindrome, and False otherwise. A palindrome reads the same
from left to right and from right to left. The empty string is a
palindrome.

Example 1:

Input: s = "aabbc"
Output: True
Explanation: "abcba" is a palindrome made of the same characters.

Example 2:

Input: s = "abc"
Output: False

Example 3:

Input: s = "carrace"
Output: True
Explanation: "racecar".

Constraints:

    0 <= len(s) <= 10^5
    s consists of printable ASCII characters. Case matters.

    REQUIRED: O(n) time, where n is the length of s. NO sorting.
"""


class Solution:
    def can_form_palindrome(self, s: str) -> bool:
        pass


sol = Solution()

print(sol.can_form_palindrome("aabbc"))  # True

# assert sol.can_form_palindrome("aabbc") is True
# assert sol.can_form_palindrome("abc") is False
# assert sol.can_form_palindrome("carrace") is True
# assert sol.can_form_palindrome("") is True
# assert sol.can_form_palindrome("a") is True
# assert sol.can_form_palindrome("ab") is False
# assert sol.can_form_palindrome("aa") is True
# assert sol.can_form_palindrome("Aa") is False
# assert sol.can_form_palindrome("aabbcd") is False
# assert sol.can_form_palindrome("abcabc") is True
# assert sol.can_form_palindrome("abcabcd") is True
# assert sol.can_form_palindrome("a b a") is True
# assert sol.can_form_palindrome("z" * 10 ** 5) is True
# assert sol.can_form_palindrome("ab" * 50000 + "c") is True
# assert sol.can_form_palindrome("ab" * 50000 + "cd") is False
# assert sol.can_form_palindrome(ascii_lowercase * 2 + "q") is True
