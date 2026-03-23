"""
URL: https://leetcode.com/problems/ransom-note/description/?envType=problem-list-v2&envId=vn57k9wr

383. Ransom Note

Given two strings ransomNote and magazine, return true if ransomNote can be constructed by using the letters from magazine and false otherwise.

Each letter in magazine can only be used once in ransomNote.

Example 1:

Input: ransomNote = "a", magazine = "b"
Output: false

Example 2:

Input: ransomNote = "aa", magazine = "ab"
Output: false

Example 3:

Input: ransomNote = "aa", magazine = "aab"
Output: true

Constraints:

    1 <= ransomNote.length, magazine.length <= 10^5
    ransomNote and magazine consist of lowercase English letters.
"""

class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        mc = Counter(magazine)
        rc = Counter(ransomNote)
        return rc - mc == {}

sol = Solution()

# print(sol.canConstruct("a", "b"))  # false

assert sol.canConstruct("a", "b") == False
assert sol.canConstruct("aa", "ab") == False
assert sol.canConstruct("aa", "aab") == True
assert sol.canConstruct("a", "a") == True
assert sol.canConstruct("ab", "ba") == True
assert sol.canConstruct("ab", "a") == False
assert sol.canConstruct("abc", "abcd") == True
assert sol.canConstruct("abc", "abd") == False
assert sol.canConstruct("aaa", "aaab") == True
assert sol.canConstruct("aaa", "aab") == False
assert sol.canConstruct("abcc", "aabbc") == False
assert sol.canConstruct("xyz", "abcdefghijklmnopqrstuvwxyzz") == True
assert sol.canConstruct("xyz", "abcdefghijklmnopqrstuvwxy") == False
assert sol.canConstruct("", "a") == True
assert sol.canConstruct("a", "") == False
assert sol.canConstruct("", "") == True
assert sol.canConstruct("hello", "olelh") == True
assert sol.canConstruct("hello", "olel") == False