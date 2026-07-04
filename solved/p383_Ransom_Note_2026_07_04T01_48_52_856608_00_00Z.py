"""
URL: https://leetcode.com/problems/ransom-note/description/?envType=problem-list-v2&envId=vn57k9wr

383. Ransom Note

Given two strings ransomNote and magazine, return true if ransomNote can be
constructed by using the letters from magazine and false otherwise.

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
        r = Counter(ransomNote)
        m = Counter(magazine)
        for l in r:
            if l not in r or m[l] < r[l]:
                return False
        return True


sol = Solution()

assert sol.canConstruct("a", "b") == False
assert sol.canConstruct("aa", "ab") == False
assert sol.canConstruct("aa", "aab") == True
assert sol.canConstruct("a", "a") == True
assert sol.canConstruct("abc", "cba") == True
assert sol.canConstruct("aab", "ab") == False
assert sol.canConstruct("aa", "aa") == True
assert sol.canConstruct("aa", "a") == False
assert sol.canConstruct("a", "aaaa") == True
assert sol.canConstruct("abcabc", "aabbcc") == True
assert sol.canConstruct("abcabc", "aabbc") == False
assert sol.canConstruct("z", "abcdefghijklmnopqrstuvwxy") == False
assert sol.canConstruct("abcdefghijklmnopqrstuvwxyz", "zyxwvutsrqponmlkjihgfedcba") == True
assert sol.canConstruct("b", "abba") == True
assert sol.canConstruct("aaaa", "aaab") == False
assert sol.canConstruct("a" * 100000, "a" * 100000) == True
assert sol.canConstruct("a" * 100000, "a" * 99999 + "b") == False