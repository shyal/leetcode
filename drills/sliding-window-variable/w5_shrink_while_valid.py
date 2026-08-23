"""
DRILL: Shrink While Valid
TRAINS: sliding-window-variable

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
    too large. Note this is the mirror of Grow and Shrink, where the loop
    runs while the window is ILLEGAL.
"""


class Solution:
    def shortestAtLeast(self, s: str, k: int) -> int:
        pass


sol = Solution()

print(sol.shortestAtLeast("abcabc", 3))  # 3

# assert sol.shortestAtLeast("abcabc", 3) == 3
# assert sol.shortestAtLeast("aaab", 2) == 2
# assert sol.shortestAtLeast("aaa", 2) == 0
# assert sol.shortestAtLeast("a", 1) == 1
# assert sol.shortestAtLeast("aaaaab", 2) == 2
# assert sol.shortestAtLeast("baaaaa", 2) == 2
# assert sol.shortestAtLeast("abababab", 2) == 2
# assert sol.shortestAtLeast("aabbccdd", 4) == 6
# assert sol.shortestAtLeast("abcdef", 6) == 6
# assert sol.shortestAtLeast("abcdef", 7) == 0
# assert sol.shortestAtLeast("zzzzabzzzz", 2) == 2
# assert sol.shortestAtLeast("aaaaaaaaab", 2) == 2
# assert sol.shortestAtLeast("abaacccb", 3) == 4
