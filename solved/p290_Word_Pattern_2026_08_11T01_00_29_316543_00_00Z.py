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
        s = s.split()
        return [pattern.index(x) for x in pattern] == [s.index(x) for x in s]


sol = Solution()

print(sol.wordPattern("abba", "dog cat cat dog"))  # True

# assert sol.wordPattern("abba", "dog cat cat dog") is True
# assert sol.wordPattern("abba", "dog cat cat fish") is False
# assert sol.wordPattern("aaaa", "dog cat cat dog") is False

# assert sol.wordPattern("a", "dog") is True
# assert sol.wordPattern("a", "dog cat") is False
# assert sol.wordPattern("ab", "dog") is False
# assert sol.wordPattern("abba", "dog cat cat") is False
# assert sol.wordPattern("abcd", "dog cat") is False

# assert sol.wordPattern("aa", "dog cat") is False
# assert sol.wordPattern("aa", "dog dog") is True
# assert sol.wordPattern("ab", "dog dog") is False
# assert sol.wordPattern("aba", "dog dog dog") is False
# assert sol.wordPattern("aaa", "dog dog dog") is True
# assert sol.wordPattern("abba", "dog dog dog dog") is False

# assert sol.wordPattern("aba", "dog cat dog") is True
# assert sol.wordPattern("abab", "dog cat dog cat") is True
# assert sol.wordPattern("aab", "dog dog cat") is True
# assert sol.wordPattern("abb", "dog cat cat") is True
# assert sol.wordPattern("abb", "dog cat dog") is False

# assert sol.wordPattern("abc", "b c a") is True
# assert sol.wordPattern("abba", "b a a b") is True
# assert sol.wordPattern("ab", "b b") is False

# assert sol.wordPattern("abcdefghijklmnopqrstuvwxyz",
#                        " ".join("w%d" % i for i in range(26))) is True
# assert sol.wordPattern("abcdefghijklmnopqrstuvwxyz",
#                        " ".join("w%d" % (i % 25) for i in range(26))) is False

# assert sol.wordPattern("ab" * 150, " ".join(["dog", "cat"] * 150)) is True
# assert sol.wordPattern("ab" * 150,
#                        " ".join(["dog", "cat"] * 149 + ["dog", "dog"])) is False
# assert sol.wordPattern("a" * 300, " ".join(["dog"] * 300)) is True
# assert sol.wordPattern("a" * 300, " ".join(["dog"] * 299 + ["cat"])) is False
# assert sol.wordPattern("a" * 300, " ".join(["dog"] * 299)) is False