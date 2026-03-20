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

    1 <= s.length, t.length <= 5 * 10^4
    s and t consist of lowercase English letters.

Follow up: What if the inputs contain Unicode characters? How would you adapt your solution to such a case?
"""

class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        return str(sorted(s)) == str(sorted(t))


sol = Solution()

print(sol.isAnagram("anagram", "nagaram"))  # true

assert sol.isAnagram("anagram", "nagaram") == True
assert sol.isAnagram("rat", "car") == False
assert sol.isAnagram("", "") == True
assert sol.isAnagram("", "a") == False
assert sol.isAnagram("a", "") == False
assert sol.isAnagram("a", "a") == True
assert sol.isAnagram("ab", "ba") == True
assert sol.isAnagram("ab", "b") == False
assert sol.isAnagram("aa", "a") == False
assert sol.isAnagram("abc", "abcd") == False
assert sol.isAnagram("aabbcc", "abcabc") == True
assert sol.isAnagram("aabbcc", "abcaac") == False
assert sol.isAnagram("abc", "def") == False
assert sol.isAnagram("aa", "bb") == False
assert sol.isAnagram("ab", "aa") == False
assert sol.isAnagram("café", "éfac") == True