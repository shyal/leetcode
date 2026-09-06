"""
DRILL: Fixed Slide
TRAINS: sliding-window-fixed

Given a string s and an integer k, return the largest number of different
characters found in any k consecutive characters of s.

Example 1:

Input: s = "abcba", k = 3
Output: 3
Explanation: the windows are "abc", "bcb" and "cba", holding 3, 2 and 3
different characters.

Example 2:

Input: s = "aaaa", k = 2
Output: 1

Example 3:

Input: s = "ab", k = 2
Output: 2
Explanation: k equals the length of s, so there is exactly one window.

Constraints:

    1 <= k <= len(s) <= 10^5
    s contains lowercase English letters.

    REQUIRED: one pass, O(n). The window's counts are MAINTAINED across
    the slide: one character enters on the right and one leaves on the
    left, and each costs O(1). Rebuilding the summary per window, with
    Counter(s[i:i+k]) or set(s[i:i+k]) or a fresh scan of the slice, is
    the failure mode this drill exists to kill. len(s) makes O(n*k) a
    TLE. A plain dict is fine, or your own dsa/sliding_window.py.
"""


class Solution:
    def maxDistinct(self, s: str, k: int) -> int:
        counter = defaultdict(int)
        left = 0
        best = 0
        for right in range(len(s)):
            counter[s[right]] += 1
            if right >= k:
                counter[s[left]] -= 1
                if counter[s[left]] == 0:
                    del counter[s[left]]
                left += 1

            best = max(len(counter), best)
        return best


sol = Solution()

print(sol.maxDistinct("abcba", 3))  # 3

assert sol.maxDistinct("abcba", 3) == 3
assert sol.maxDistinct("aaaa", 2) == 1
assert sol.maxDistinct("ab", 2) == 2
assert sol.maxDistinct("a", 1) == 1
assert sol.maxDistinct("abcde", 1) == 1
assert sol.maxDistinct("abcde", 5) == 5
assert sol.maxDistinct("aabbcc", 2) == 2
assert sol.maxDistinct("aabbcc", 3) == 2
assert sol.maxDistinct("aabbcc", 4) == 3
assert sol.maxDistinct("abaabbab", 3) == 2
assert sol.maxDistinct("zzzzab", 3) == 3
assert sol.maxDistinct("abcabcabc", 4) == 3
