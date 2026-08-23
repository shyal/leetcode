"""
URL: https://leetcode.com/problems/rotate-string/description/?envType=problem-list-v2&envId=vn57k9wr

796. Rotate String

Given two strings s and goal, return true if and only if s can become goal after some number of shifts on s.

A shift on s consists of moving the leftmost character of s to the rightmost position.

For example, if s = "abcde", then it will be "bcdea" after one shift.

Example 1:

Input: s = "abcde", goal = "cdeab"
Output: true

Example 2:

Input: s = "abcde", goal = "abced"
Output: false

Constraints:

    1 <= s.length, goal.length <= 100
    s and goal consist of lowercase English letters.
"""


class Solution:
    def rotateString(self, s: str, goal: str) -> bool:
        if len(s) == len(goal) == 0:
            return True

        def rotate():
            return s[1:] + s[0]

        for _ in range(len(s)):
            if s == goal:
                return True
            s = rotate()

        return False


sol = Solution()

print(sol.rotateString("abcde", "cdeab"))  # True

assert sol.rotateString("abcde", "cdeab") == True
assert sol.rotateString("abcde", "abced") == False
assert sol.rotateString("m", "f") == False
assert sol.rotateString("c", "w") == False

assert Solution().rotateString("", "") == True
assert Solution().rotateString("a", "a") == True
assert Solution().rotateString("a", "b") == False
assert Solution().rotateString("aaaaa", "aaaaa") == True
assert Solution().rotateString("aaaaa", "aaaab") == False
assert Solution().rotateString("abcabcabc", "bcabcabca") == True
assert Solution().rotateString("abcabcabc", "cabcabcab") == True
assert Solution().rotateString("abcabcabc", "abcabcabc") == True
assert Solution().rotateString("abcabcabc", "acbabcabc") == False
assert Solution().rotateString("z" * 100, "z" * 100) == True
assert Solution().rotateString("z" * 99 + "y", "y" + "z" * 99) == True
assert (
    Solution().rotateString(
        "abcdefghijklmnopqrstuvwxyz" * 4,
        "defghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabc",
    )
    == False
)
