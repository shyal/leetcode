"""
DRILL: Exactly K
TRAINS: sliding-window-variable

Given a string s and an integer k, return how many substrings of s hold
exactly k different characters.

Example 1:

Input: s = "abca", k = 2
Output: 3
Explanation: the substrings holding exactly 2 different characters are
"ab", "bc" and "ca".

Example 2:

Input: s = "aaa", k = 1
Output: 6
Explanation: all 6 substrings hold one character.

Example 3:

Input: s = "abc", k = 3
Output: 1
Explanation: only the whole string holds 3 different characters.

Constraints:

    1 <= k <= 26
    1 <= len(s) <= 10^5
    s contains lowercase English letters.

    REQUIRED: O(n) overall. Any helper you lean on is written here, not
    pasted from Count by Contribution. Listing the substrings and
    counting them one by one is O(n^2) and the failure mode this drill
    exists to kill.
"""


class Solution:
    def exactly(self, s: str, k: int) -> int:
        pass


sol = Solution()

print(sol.exactly("abca", 2))  # 3

# assert sol.exactly("abca", 2) == 3
# assert sol.exactly("aaa", 1) == 6
# assert sol.exactly("abc", 3) == 1
# assert sol.exactly("a", 1) == 1
# assert sol.exactly("abc", 1) == 3
# assert sol.exactly("abc", 2) == 2
# assert sol.exactly("aabb", 1) == 6
# assert sol.exactly("aabb", 2) == 4
# assert sol.exactly("abab", 1) == 4
# assert sol.exactly("abab", 2) == 6
# assert sol.exactly("zzzz", 2) == 0
# assert sol.exactly("abcde", 5) == 1
# assert sol.exactly("pqpqs", 2) == 7
