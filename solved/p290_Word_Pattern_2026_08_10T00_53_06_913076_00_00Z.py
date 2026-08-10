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
    - 'a' maps to "dog".
    - 'b' maps to "cat".

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
"""


class Solution:
    def wordPattern(self, pattern: str, s: str) -> bool:
        words = s.split()
        return [pattern.index(x) for x in pattern] == [words.index(x) for x in words]


sol = Solution()

# print(sol.wordPattern("abba", "dog cat cat dog"))  # True

assert sol.wordPattern("abba", "dog cat cat dog") == True
assert sol.wordPattern("abba", "dog cat cat fish") == False
assert sol.wordPattern("aaaa", "dog cat cat dog") == False

assert sol.wordPattern("a", "dog") == True
assert sol.wordPattern("a", "dog cat") == False
assert sol.wordPattern("ab", "dog") == False
assert sol.wordPattern("aa", "dog dog") == True
assert sol.wordPattern("aa", "dog cat") == False
assert sol.wordPattern("ab", "dog dog") == False
assert sol.wordPattern("ab", "dog cat") == True
assert sol.wordPattern("abc", "dog cat bird") == True
assert sol.wordPattern("aba", "cat dog cat") == True
assert sol.wordPattern("aba", "cat dog dog") == False
assert sol.wordPattern("abab", "dog cat dog cat") == True
assert sol.wordPattern("abab", "dog cat dog dog") == False
assert sol.wordPattern("aaa", "dog dog dog") == True
assert sol.wordPattern("abba", "dog dog dog dog") == False
assert sol.wordPattern("abca", "dog cat bird dog") == True
assert sol.wordPattern("abcd", "dog cat bird dog") == False
assert sol.wordPattern("abcb", "dog cat bird cat") == True
assert sol.wordPattern("abcb", "dog cat bird dog") == False
assert sol.wordPattern("aabb", "dog dog cat cat") == True
assert sol.wordPattern("aabb", "dog dog dog cat") == False
assert sol.wordPattern("abbc", "dog cat cat dog") == False
assert sol.wordPattern("baba", "dog cat dog cat") == True
assert sol.wordPattern("he", "unit") == False
assert sol.wordPattern("aaa", "aa aa aa") == True
assert sol.wordPattern("ab", "a b") == True
assert sol.wordPattern("ab", "b a") == True
assert sol.wordPattern("aba", "a b a") == True
assert sol.wordPattern("abc", "b c a") == True
assert sol.wordPattern("a", "a") == True
assert sol.wordPattern("b", "a") == True
assert sol.wordPattern("abcdefghijklmnopqrstuvwxyz", " ".join(chr(ord("a") + i) * 2 for i in range(26))) == True
assert sol.wordPattern("ab" * 150, " ".join(["dog", "cat"] * 150)) == True
assert sol.wordPattern("ab" * 150, " ".join(["dog", "cat"] * 149 + ["dog", "dog"])) == False
assert sol.wordPattern("a" * 300, " ".join(["dog"] * 300)) == True
assert sol.wordPattern("a" * 300, " ".join(["dog"] * 299 + ["cat"])) == False
assert sol.wordPattern("ab" * 150, " ".join(["dog", "cat"] * 149 + ["dog"])) == False