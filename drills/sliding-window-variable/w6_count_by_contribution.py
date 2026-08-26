"""
DRILL: Count by Contribution
TRAINS: sliding-window-variable

Given a string s and an integer k, return how many substrings of s hold
at most k different characters. Two substrings at different positions
count separately even when they read the same.

Example 1:

Input: s = "abca", k = 2
Output: 7
Explanation: the substrings are "a", "ab", "b", "bc", "c", "ca" and the
final "a". Every other substring holds 3 different characters.

Example 2:

Input: s = "aaa", k = 1
Output: 6
Explanation: every one of the 6 substrings holds one character.

Example 3:

Input: s = "abc", k = 3
Output: 6
Explanation: k is large enough that every substring qualifies.

Constraints:

    1 <= k <= 26
    1 <= len(s) <= 10^5
    s contains lowercase English letters.

    REQUIRED: one pass, O(n). The window's counts are maintained by one
    add and one remove, never rebuilt. Listing the legal substrings and
    counting them one by one is O(n^2) and is the failure mode this drill
    exists to kill. len(s) makes it a TLE.
"""


class Solution:
    def countAtMost(self, s: str, k: int) -> int:
        pass


sol = Solution()

print(sol.countAtMost("abca", 2))  # 7

# assert sol.countAtMost("abca", 2) == 7
# assert sol.countAtMost("aaa", 1) == 6
# assert sol.countAtMost("abc", 3) == 6
# assert sol.countAtMost("a", 1) == 1
# assert sol.countAtMost("abc", 1) == 3
# assert sol.countAtMost("abc", 2) == 5
# assert sol.countAtMost("aabb", 1) == 6
# assert sol.countAtMost("aabb", 2) == 10
# assert sol.countAtMost("abab", 1) == 4
# assert sol.countAtMost("abab", 2) == 10
# assert sol.countAtMost("abcde", 1) == 5
# assert sol.countAtMost("zzzz", 2) == 10
