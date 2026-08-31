"""
DRILL: Substrings by End
TRAINS: substring-enumeration

Given a string s, return every substring of s, grouped by where it
ends: every substring ending at index 0, then every substring ending at
index 1 from longest (starting at index 0) to shortest, and so on. Two
substrings that read the same but sit at different positions are two
entries.

Example 1:

Input: s = "abc"
Output: ["a", "ab", "b", "abc", "bc", "c"]
Explanation: the substrings ending at index 2 are "abc", "bc" and "c",
in that order.

Example 2:

Input: s = "aaa"
Output: ["a", "aa", "a", "aaa", "aa", "a"]

Constraints:

    1 <= len(s) <= 100
    s contains lowercase English letters.

    REQUIRED: len(s) * (len(s) + 1) / 2 entries, one per position, in
    the stated order. NO set, NO deduplication: dropping a repeat is the
    failure mode this drill exists to kill, and every count built on
    this list comes out short.

Note: "everything that ends here, over its starts" is the loop of the
counting window (713, 992, 2962, 3258) and of every prefix DP where the
value at an end is a max or a sum over its starts (91, 139, 300). Those
problems are this loop with a rule in the inner body.
"""


class Solution:
    def substringsByEnd(self, s: str) -> list[str]:
        pass


sol = Solution()

print(sol.substringsByEnd("abc"))  # ['a', 'ab', 'b', 'abc', 'bc', 'c']

# assert sol.substringsByEnd("abc") == ["a", "ab", "b", "abc", "bc", "c"]
# assert sol.substringsByEnd("aaa") == ["a", "aa", "a", "aaa", "aa", "a"]
# assert sol.substringsByEnd("a") == ["a"]
# assert sol.substringsByEnd("ab") == ["a", "ab", "b"]
# assert sol.substringsByEnd("abca") == ["a", "ab", "b", "abc", "bc", "c", "abca", "bca", "ca", "a"]
# assert len(sol.substringsByEnd("abcdefghij")) == 55
