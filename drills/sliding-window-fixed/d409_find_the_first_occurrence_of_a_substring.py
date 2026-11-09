"""
EPI 6.12 Find the first occurrence of a substring

Given a text t and a pattern s, return the smallest index i such that
t[i:i + len(s)] == s. Return -1 when s does not occur in t. An empty
pattern occurs at index 0. Use the Rabin-Karp algorithm.

Example 1:

Input: t = "hello world", s = "world"
Output: 6

Example 2:

Input: t = "abab", s = "ba"
Output: 1

Example 3:

Input: t = "abc", s = "d"
Output: -1

Constraints:

    0 <= len(t), len(s) <= 2 * 10^5
    t and s consist of ASCII characters.

    REQUIRED: O(m + n) expected time, where m = len(t) and n = len(s).
    NO find(), index(), count(), startswith(), NO `in` on strings, NO
    regex.
"""


class Solution:
    def rabin_karp(self, t: str, s: str) -> int:
        pass


sol = Solution()

print(sol.rabin_karp("hello world", "world"))  # 6

# assert sol.rabin_karp("hello world", "world") == 6
# assert sol.rabin_karp("abab", "ba") == 1
# assert sol.rabin_karp("abc", "d") == -1
# assert sol.rabin_karp("abc", "") == 0
# assert sol.rabin_karp("", "") == 0
# assert sol.rabin_karp("", "a") == -1
# assert sol.rabin_karp("a", "a") == 0
# assert sol.rabin_karp("ab", "abc") == -1
# assert sol.rabin_karp("abab", "ab") == 0
# assert sol.rabin_karp("aaab", "ab") == 2
# assert sol.rabin_karp("abc", "c") == 2
# assert sol.rabin_karp("abc", "abc") == 0
# assert sol.rabin_karp("xyzxyz", "zx") == 2
# assert sol.rabin_karp("a" * 200000, "a" * 100000 + "b") == -1
# assert sol.rabin_karp("a" * 199999 + "b", "a" * 100000 + "b") == 99999
# assert sol.rabin_karp("ab" * 100000, "ba" * 1000) == 1
