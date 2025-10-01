"""
URL: https://leetcode.com/problems/rotate-string/description/

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

from itertools import islice, chain


class Solution:
    def rotateString(self, s: str, goal: str) -> bool:
        if s == goal:
            return True

        if len(s) != len(goal):
            return False

        def rotate(s, r):
            return chain(islice(s, r, None), islice(s, None, r))

        for shift in range(len(s)):
            r = rotate(s, shift)
            if all(a == b for a, b in zip(r, goal)):
                return True

        return False


sol = Solution()
assert sol.rotateString(s="abcde", goal="cdeab") == True
assert sol.rotateString(s="abcd", goal="cdeab") == False
assert sol.rotateString(s="123", goal="124") == False
assert sol.rotateString(s="", goal="") == True
assert sol.rotateString(s="hello", goal="lohel") == True
