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


Follow up: What if the inputs contain Unicode characters? How would you adapt your
solution to such a case?
"""

class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        sc = Counter(s)
        tc = Counter(t)
        return sc == tc


sol = Solution()

print(sol.isAnagram("anagram", "nagaram"))  # True

assert sol.isAnagram("anagram", "nagaram") == True
assert sol.isAnagram("rat", "car") == False
assert sol.isAnagram("a", "a") == True
assert sol.isAnagram("a", "b") == False
assert sol.isAnagram("ab", "abc") == False
assert sol.isAnagram("abc", "ab") == False
assert sol.isAnagram("aacc", "ccac") == False
assert sol.isAnagram("aabb", "bbaa") == True
assert sol.isAnagram("listen", "silent") == True
assert sol.isAnagram("aaa", "aa") == False
assert sol.isAnagram("same", "same") == True
assert sol.isAnagram("ab" * 25000, "ba" * 25000) == True
assert sol.isAnagram("a" * 50000, "a" * 49999 + "b") == False