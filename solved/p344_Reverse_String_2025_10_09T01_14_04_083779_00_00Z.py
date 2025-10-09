"""
URL: https://leetcode.com/problems/reverse-string/description/

344. Reverse String

Write a function that reverses a string. The input string is given as an array of characters s.

You must do this by modifying the input array in-place with O(1) extra memory.

Example 1:

Input: s = ["h","e","l","l","o"]
Output: ["o","l","l","e","h"]

Example 2:

Input: s = ["H","a","n","n","a","h"]
Output: ["h","a","n","n","a","H"]

Constraints:

    1 <= s.length <= 10^5
    s[i] is a printable ascii character.
"""

from typing import List


class Solution:
    def reverseString(self, s: List[str]) -> None:
        for i in range(len(s) // 2):
            s[i], s[~i] = s[~i], s[i]


sol = Solution()

s = ["h", "e", "l", "l", "o"]
sol.reverseString(s)
# print(s)  # ["o","l","l","e","h"]

s = ["h", "e", "l", "l", "o"]
sol.reverseString(s)
assert s == ["o", "l", "l", "e", "h"]
s = ["H", "a", "n", "n", "a", "h"]
sol.reverseString(s)
assert s == ["h", "a", "n", "n", "a", "H"]
s = ["a"]
sol.reverseString(s)
assert s == ["a"]
s = ["a", "b"]
sol.reverseString(s)
assert s == ["b", "a"]
s = ["a", "b", "c"]
sol.reverseString(s)
assert s == ["c", "b", "a"]
s = ["!", "@", "#", "$"]
sol.reverseString(s)
assert s == ["$", "#", "@", "!"]
s = ["x", "x", "x", "x"]
sol.reverseString(s)
assert s == ["x", "x", "x", "x"]
s = ["a", "b", "a"]
sol.reverseString(s)
assert s == ["a", "b", "a"]
s = ["1", "2", "3", "4", "5", "6", "7"]
sol.reverseString(s)
assert s == ["7", "6", "5", "4", "3", "2", "1"]
