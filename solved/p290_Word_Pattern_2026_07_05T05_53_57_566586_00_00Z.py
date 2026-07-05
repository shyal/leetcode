"""
URL: https://leetcode.com/problems/word-pattern/description/?envType=problem-list-v2&envId=vn57k9wr

290. Word Pattern

Given a pattern and a string s, find if s follows the same pattern.

Here follow means a full match, such that there is a bijection between a letter
in pattern and a non-empty word in s. Specifically:

    - Each letter in pattern maps to exactly one unique word in s.
    - Each unique word in s maps to exactly one letter in pattern.
    - No two letters map to the same word, and no two words map to the same letter.


Example 1:

Input: pattern = "abba", s = "dog cat cat dog"
Output: true
Explanation:
The bijection can be established as:
    'a' maps to "dog".
    'b' maps to "cat".

Example 2:

Input: pattern = "abba", s = "dog cat cat fish"
Output: false

Example 3:

Input: pattern = "aaaa", s = "dog cat cat dog"
Output: false


Constraints:

    1 <= pattern.length <= 300
    pattern contains only lower-case English letters.
    1 <= s.length <= 3000
    s contains only lowercase English letters and spaces ' '.
    s does not contain any leading or trailing spaces.
    All the words in s are separated by a single space.


---

Not too far from solve, but proper breakfast is needed.

"""

class Solution:
    def wordPattern(self, pattern: str, s: str) -> bool:
        d = {
        }
        words = s.split()
        if len(words) != len(pattern):
            return False
        for letter, word in zip(pattern, words):
            if letter in d:
                if d[letter] != word:
                    return False
            else:
                if word in d.values():
                    return False
                d[letter] = word
        return True


sol = Solution()

assert sol.wordPattern("abba", "dog cat cat dog") == True
assert sol.wordPattern("abba", "dog cat cat fish") == False
assert sol.wordPattern("aaaa", "dog cat cat dog") == False
assert sol.wordPattern("a", "dog") == True
assert sol.wordPattern("a", "dog cat") == False
assert sol.wordPattern("aaa", "dog dog") == False
assert sol.wordPattern("ab", "dog dog") == False
assert sol.wordPattern("aa", "dog cat") == False
assert sol.wordPattern("aaa", "dog dog dog") == True
assert sol.wordPattern("abc", "dog cat fish") == True
assert sol.wordPattern("abc", "dog cat dog") == False
assert sol.wordPattern("abab", "dog cat dog cat") == True
assert sol.wordPattern("abba", "a b b a") == True
assert sol.wordPattern("abba", "b a a b") == True
assert sol.wordPattern("aba", "dog cat cat") == False
assert sol.wordPattern("aab", "cat cat cat") == False