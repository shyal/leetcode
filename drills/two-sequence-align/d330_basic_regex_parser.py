"""
Given a string text and a string pattern, return True when pattern
matches the whole of text, and False when it does not. In pattern, a
"." matches any one character, and a "*" after a character matches zero
or more repeats of that character. Every other character of pattern
matches itself only.

Example 1:

Input: text = "abbdbb", pattern = "ab*d"
Output: False
Explanation: "ab*d" matches "abbd", but the text has "bb" after it.

Example 2:

Input: text = "acd", pattern = "ab*c."
Output: True
Explanation: "b*" matches zero letters b, "c" matches "c", "." matches
"d".

Example 3:

Input: text = "", pattern = "a*"
Output: True

Constraints:

    0 <= len(text) <= 20
    0 <= len(pattern) <= 20
    text holds lowercase letters only.
    pattern holds lowercase letters, "." and "*". A "*" never stands
    first and never follows another "*".

    REQUIRED: O(len(text) * len(pattern)) time. NO re module, NO
    expansion of "*" into candidate strings.
"""


class Solution:
    def is_match(self, text: str, pattern: str) -> bool:
        pass


sol = Solution()

print(sol.is_match("abbdbb", "ab*d"))  # False

# assert sol.is_match("abbdbb", "ab*d") is False
# assert sol.is_match("acd", "ab*c.") is True
# assert sol.is_match("", "a*") is True
# assert sol.is_match("", "") is True
# assert sol.is_match("aa", "a") is False
# assert sol.is_match("bb", "bb") is True
# assert sol.is_match("aba", "a.a") is True
# assert sol.is_match("abaa", "a.*a*") is True
# assert sol.is_match("a", "") is False
# assert sol.is_match("a", ".") is True
# assert sol.is_match("ab", ".*") is True
# assert sol.is_match("ab", ".*c") is False
# assert sol.is_match("aaa", "a*a") is True
# assert sol.is_match("mississippi", "mis*is*p*.") is False
# assert sol.is_match("mississippi", "mis*is*ip*i") is True
# assert sol.is_match("a" * 20, "a*a*a*a*a*a*a*a*a*b") is False
# assert sol.is_match("a" * 20, "a*a*a*a*a*a*a*a*a*a*") is True
