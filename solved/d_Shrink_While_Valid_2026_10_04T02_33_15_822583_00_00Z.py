"""
DRILL: Shrink While Valid

Given a string s and an integer k, return the length of the shortest
substring of s that holds at least k different characters. Return 0 if no
substring holds that many.

Example 1:

Input: s = "abcabc", k = 3
Output: 3
Explanation: "abc" holds 3 different characters and nothing shorter does.

Example 2:

Input: s = "aaab", k = 2
Output: 2
Explanation: the shortest is "ab" at the end.

Example 3:

Input: s = "aaa", k = 2
Output: 0
Explanation: s holds only one different character.

Constraints:

    1 <= k <= 26
    1 <= len(s) <= 10^5
    s contains lowercase English letters.

    REQUIRED: one pass, O(n). Both ends of the window move forward only.
    The window's counts are maintained by one add and one remove, never
    rebuilt. A legal window can hold a shorter legal window inside it, so
    measuring a window the moment it first becomes legal is the failure
    mode this drill exists to kill: it silently returns lengths that are
    too large.
---
Solved. The tricky part was figuring out / remembering that the 
if len(count) == k
  best = min(best, (right - left + 1))
goes inside the while loop
"""


# mu 0.7
# def shortestAtLeast(s: str, k: int) -> int
#   best, left, count = inf, 0, Multiset()
#   for right, v in s
#     count[v] += 1
#     while len(count) >= k
#       if len(count) == k
#         best = min(best, (right - left + 1))
#       count[s[left]] -=1
#       left += 1
#
#   best or 0 if best == inf

from collections import Counter
from math import inf


class Multiset(Counter):
    def __setitem__(self, key, value):
        if value == 0:
            self.pop(key, None)
        else:
            super().__setitem__(key, value)

    def update(self, iterable=None, /, **kwds):
        super().update(iterable, **kwds)
        for key in [k for k, v in self.items() if v == 0]:
            del self[key]


class Solution:
    def shortestAtLeast(self, s: str, k: int) -> int:
        best, left, count = inf, 0, Multiset()
        for right, v in enumerate(s):
            count[v] += 1
            while len(count) >= k:
                if len(count) == k:
                    best = min(best, (right - left + 1))
                count[s[left]] -= 1
                left += 1
        return (0 if best == best == inf else best)


sol = Solution()
print(sol.shortestAtLeast('abcabc', 3))
assert sol.shortestAtLeast('abcabc', 3) == 3
assert sol.shortestAtLeast('aaab', 2) == 2
assert sol.shortestAtLeast('aaa', 2) == 0
assert sol.shortestAtLeast('a', 1) == 1
assert sol.shortestAtLeast('aaaaab', 2) == 2
assert sol.shortestAtLeast('baaaaa', 2) == 2
assert sol.shortestAtLeast('abababab', 2) == 2
assert sol.shortestAtLeast('aabbccdd', 4) == 6
assert sol.shortestAtLeast('abcdef', 6) == 6
assert sol.shortestAtLeast('abcdef', 7) == 0
assert sol.shortestAtLeast('zzzzabzzzz', 2) == 2
assert sol.shortestAtLeast('aaaaaaaaab', 2) == 2
assert sol.shortestAtLeast('abaacccb', 3) == 4
