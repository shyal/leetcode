"""
DRILL: All Substrings
TRAINS: substring-enumeration

Given a string s, return every substring of s, grouped by where it
starts: every substring starting at index 0 from shortest to longest,
then every substring starting at index 1, and so on. Two substrings
that read the same but sit at different positions are two entries.

Example 1:

Input: s = "abc"
Output: ["a", "ab", "abc", "b", "bc", "c"]

Example 2:

Input: s = "aaa"
Output: ["a", "aa", "aaa", "a", "aa", "a"]
Explanation: six positions, six entries, three distinct strings.

Constraints:

    1 <= len(s) <= 100
    s contains lowercase English letters.

    REQUIRED: len(s) * (len(s) + 1) / 2 entries, one per position, in
    the stated order. NO set, NO deduplication: dropping a repeat is the
    failure mode this drill exists to kill, and every count built on
    this list comes out short.

Note: this loop is the brute force under most substring and subarray
problems (3, 5, 53, 209, 560, 647). Write it first to see the answer,
then replace the inner loop with the technique.
"""


class Solution:
    def allSubstrings(self, s: str) -> list[str]:
        res = []
        for i in range(len(s)):
            for j in range(i, len(s)):
                res.append(s[i : j + 1])
        return res


sol = Solution()

print(sol.allSubstrings("abc"))  # ['a', 'ab', 'abc', 'b', 'bc', 'c']

assert sol.allSubstrings("abc") == ["a", "ab", "abc", "b", "bc", "c"]
assert sol.allSubstrings("aaa") == ["a", "aa", "aaa", "a", "aa", "a"]
assert sol.allSubstrings("a") == ["a"]
assert sol.allSubstrings("ab") == ["a", "ab", "b"]
assert sol.allSubstrings("abca") == [
    "a",
    "ab",
    "abc",
    "abca",
    "b",
    "bc",
    "bca",
    "c",
    "ca",
    "a",
]
assert len(sol.allSubstrings("abcdefghij")) == 55
