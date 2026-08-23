"""
DRILL: Anagram Windows
TRAINS: sliding-window-fixed

Given two strings s and t, return how many substrings of s have length
len(t) and hold exactly the characters of t, counting duplicates. Order
does not matter, so a window qualifies when it is a rearrangement of t.

Example 1:

Input: s = "cbaebabacd", t = "abc"
Output: 2
Explanation: the windows "cba" at index 0 and "bac" at index 6 are
rearrangements of "abc".

Example 2:

Input: s = "abab", t = "ab"
Output: 3
Explanation: "ab", "ba" and "ab" all qualify. Windows at different
positions count separately.

Example 3:

Input: s = "a", t = "aa"
Output: 0
Explanation: t is longer than s, so there is no window to test.

Constraints:

    1 <= len(s), len(t) <= 10^5
    s and t contain lowercase English letters.

    REQUIRED: one pass, O(len(s)). The window slides by one character
    entering and one leaving, each O(1). Comparing two tallies per
    window, with Counter(window) == Counter(t), or sorting the window,
    is the failure mode this drill exists to kill: both cost O(k) or
    worse at every position. Collapse the comparison to a single integer
    that tracks how many characters of t currently sit at exactly the
    amount t asks for. A window qualifies when that integer says every
    character of t does.
"""


class Solution:
    def countAnagramWindows(self, s: str, t: str) -> int:
        pass


sol = Solution()

print(sol.countAnagramWindows("cbaebabacd", "abc"))  # 2

# assert sol.countAnagramWindows("cbaebabacd", "abc") == 2
# assert sol.countAnagramWindows("abab", "ab") == 3
# assert sol.countAnagramWindows("a", "aa") == 0
# assert sol.countAnagramWindows("aa", "a") == 2
# assert sol.countAnagramWindows("abc", "abc") == 1
# assert sol.countAnagramWindows("abc", "cba") == 1
# assert sol.countAnagramWindows("aaaa", "aa") == 3
# assert sol.countAnagramWindows("aaaa", "ab") == 0
# assert sol.countAnagramWindows("baa", "aa") == 1
# assert sol.countAnagramWindows("abcdefg", "gf") == 1
# assert sol.countAnagramWindows("xyzxyz", "zyx") == 4
# assert sol.countAnagramWindows("aabbaa", "aab") == 2
