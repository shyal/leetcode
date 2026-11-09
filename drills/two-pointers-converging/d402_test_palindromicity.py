"""
EPI 6.5 Test palindromicity

Given a string s, return True when s is a palindrome after you drop
every character that is not a letter or a digit and ignore case.
Return False otherwise.

Example 1:

Input: s = "Was it a car or a cat I saw?"
Output: True
Explanation: the letters are "wasitacaroracatisaw", which reads the
same in both directions.

Example 2:

Input: s = "Race a car"
Output: False

Example 3:

Input: s = ".,!"
Output: True
Explanation: no letters or digits remain, and the empty string is a
palindrome.

Constraints:

    0 <= len(s) <= 2 * 10^5
    s consists of printable ASCII characters.

    REQUIRED: O(n) time, O(1) extra space. NO new string or list, NO
    slicing, NO reversed(), NO filter().
"""


class Solution:
    def is_palindrome(self, s: str) -> bool:
        pass


sol = Solution()

print(sol.is_palindrome("Was it a car or a cat I saw?"))  # True

# assert sol.is_palindrome("Was it a car or a cat I saw?") is True
# assert sol.is_palindrome("Race a car") is False
# assert sol.is_palindrome(".,!") is True
# assert sol.is_palindrome("") is True
# assert sol.is_palindrome("a") is True
# assert sol.is_palindrome("ab") is False
# assert sol.is_palindrome("Aa") is True
# assert sol.is_palindrome("0P") is False
# assert sol.is_palindrome("1a1") is True
# assert sol.is_palindrome("No 'x' in Nixon") is True
# assert sol.is_palindrome(".a") is True
# assert sol.is_palindrome("a.") is True
# assert sol.is_palindrome("ab.") is False
# assert sol.is_palindrome("!b, a?") is False
# assert sol.is_palindrome("a" * 100000 + ", " * 1000 + "A" * 100000) is True
# assert sol.is_palindrome("a" * 100000 + "b" + "a" * 99999) is False
# assert sol.is_palindrome("?" * 200000) is True
