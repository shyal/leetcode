"""
Earliest Indices Of A Subsequence

Given two strings sub and s, where sub is a subsequence of s, return
the list res of len(sub) indices of s such that s[res[i]] == sub[i].
The indices in res are strictly increasing, and each index is the
smallest possible.

Example 1:

Input: sub = "cbc", s = "cbcdbc"
Output: [0, 1, 2]
Explanation: s[0] = "c", s[1] = "b" and s[2] = "c".

Example 2:

Input: sub = "cbc", s = "cabcdbc"
Output: [0, 2, 3]
Explanation: s[0] = "c", s[2] = "b" and s[3] = "c".

Example 3:

Input: sub = "d", s = "abcd"
Output: [3]

Constraints:

    1 <= len(sub) <= len(s) <= 10^5
    sub and s consist of lowercase English letters.
    sub is a subsequence of s.

    REQUIRED: O(len(sub) + len(s)) time. NO while loop.
"""


class Solution:
    def earliest_indices(self, sub: str, s: str) -> list[int]:
        pass


sol = Solution()

print(sol.earliest_indices("cbc", "cbcdbc"))  # [0, 1, 2]

# assert sol.earliest_indices("cbc", "cbcdbc") == [0, 1, 2]
# assert sol.earliest_indices("cbc", "cabcdbc") == [0, 2, 3]
# assert sol.earliest_indices("d", "abcd") == [3]
# assert sol.earliest_indices("a", "a") == [0]
# assert sol.earliest_indices("aa", "aaaa") == [0, 1]
# assert sol.earliest_indices("xyz", "xyzz") == [0, 1, 2]
# assert sol.earliest_indices("ab", "ba" * 4) == [1, 2]
# assert sol.earliest_indices("abc", "aabbcc") == [0, 2, 4]
# assert sol.earliest_indices("ace", "abcde") == [0, 2, 4]
# assert sol.earliest_indices("abcd", "abcd") == [0, 1, 2, 3]
# assert sol.earliest_indices("ba", "aaab" + "a") == [3, 4]
# assert sol.earliest_indices("zz", "z" + "a" * 99998 + "z") == [0, 99999]
# assert sol.earliest_indices("a" * 10 ** 5, "a" * 10 ** 5) == list(range(10 ** 5))
# assert sol.earliest_indices("ab" * 50000, "ab" * 50000) == list(range(10 ** 5))
# assert sol.earliest_indices("b" * 300, "a" * 99700 + "b" * 300) == list(range(99700, 10 ** 5))
