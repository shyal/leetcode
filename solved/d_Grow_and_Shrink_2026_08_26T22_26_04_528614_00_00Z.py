"""
DRILL: Grow and Shrink
TRAINS: sliding-window-variable

Given a string s and an integer k, return the length of the longest
substring of s that holds at most k different characters.

Example 1:

Input: s = "eceba", k = 2
Output: 3
Explanation: "ece" holds 2 different characters. No longer substring
holds 2 or fewer.

Example 2:

Input: s = "aa", k = 1
Output: 2

Example 3:

Input: s = "abc", k = 0
Output: 0
Explanation: no substring of length 1 or more holds 0 different
characters.

Constraints:

    0 <= k <= 26
    1 <= len(s) <= 10^5
    s contains lowercase English letters.

    REQUIRED: one pass, O(n). Both ends of the window move forward only
    and never move backward. The window's counts are maintained by one
    add and one remove, never rebuilt. Measuring a window that is not
    legal is the failure mode this drill exists to kill: the answers
    come back silently too large.
"""


class Solution:
    def longestAtMost(self, s: str, k: int) -> int:
        best = 0
        count = defaultdict(int)
        left = 0
        for right, v in enumerate(s):
            count[v] += 1
            if len(count) > k:
                count[s[left]] -= 1
                if count[s[left]] == 0:
                    del count[s[left]]
                left += 1
            best = max(best, right - left + 1)
        return best


sol = Solution()

print(sol.longestAtMost("eceba", 2))  # 3

assert sol.longestAtMost("eceba", 2) == 3
assert sol.longestAtMost("aa", 1) == 2
assert sol.longestAtMost("abc", 0) == 0
assert sol.longestAtMost("a", 1) == 1
assert sol.longestAtMost("abcabcabc", 3) == 9
assert sol.longestAtMost("abaccc", 2) == 4
assert sol.longestAtMost("aabbcc", 1) == 2
assert sol.longestAtMost("aabbcc", 2) == 4
assert sol.longestAtMost("aabbcc", 3) == 6
assert sol.longestAtMost("abcdef", 1) == 1
assert sol.longestAtMost("wwwwwwww", 5) == 8
assert sol.longestAtMost("abaccccdd", 3) == 7
