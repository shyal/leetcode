"""
URL: https://leetcode.com/problems/valid-anagram/description/?envType=problem-list-v2&envId=vn57k9wr

242. Valid Anagram

Given two strings s and t, return true if t is an anagram of s, and false otherwise.


Example 1:

Input: s = "anagram", t = "nagaram"

Output: true

Example 2:

Input: s = "rat", t = "car"

Output: false


Constraints:

    1 <= s.length, t.length <= 5 * 104
    s and t consist of lowercase English letters.


Follow up: What if the inputs contain Unicode characters? How would you adapt your solution to such a case?
"""

from collections import Counter


class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        return Counter(s) == Counter(t)


sol = Solution()
assert sol.isAnagram("anagram", "nagaram") == True

sol = Solution()
assert sol.isAnagram("rat", "car") == False
