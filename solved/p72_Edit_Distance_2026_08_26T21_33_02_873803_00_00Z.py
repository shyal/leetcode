"""
URL: https://leetcode.com/problems/edit-distance/description/?envType=problem-list-v2&envId=vn57k9wr

72. Edit Distance

Given two strings word1 and word2, return the minimum number of operations required to convert word1 to word2.

You have the following three operations permitted on a word:

- Insert a character
- Delete a character
- Replace a character

Example 1:

Input: word1 = "horse", word2 = "ros"
Output: 3
Explanation:
horse -> rorse (replace 'h' with 'r')
rorse -> rose (remove 'r')
rose -> ros (remove 'e')

Example 2:

Input: word1 = "intention", word2 = "execution"
Output: 5
Explanation:
intention -> inention (remove 't')
inention -> enention (replace 'i' with 'e')
enention -> exention (replace 'n' with 'x')
exention -> exection (replace 'n' with 'c')
exection -> execution (insert 'u')

Constraints:

    0 <= word1.length, word2.length <= 500
    word1 and word2 consist of lowercase English letters.
"""


class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        @cache
        def DP(a, b):
            if len(a) == 0 or len(b) == 0:
                return len(a) or len(b)
            if a[-1] == b[-1]:
                return DP(a[:-1], b[:-1])
            dela = DP(a, b[:-1])
            delb = DP(a[:-1], b)
            sub = DP(a[:-1], b[:-1])
            return min([dela, delb, sub]) + 1

        return DP(word1, word2)


sol = Solution()

print(sol.minDistance("horse", "ros"))  # 3

assert sol.minDistance("horse", "ros") == 3
assert sol.minDistance("intention", "execution") == 5

assert sol.minDistance("", "") == 0
assert sol.minDistance("a", "") == 1
assert sol.minDistance("", "a") == 1
assert sol.minDistance("abc", "abc") == 0
assert sol.minDistance("abc", "def") == 3
assert sol.minDistance("aaaaa", "aaa") == 2
assert sol.minDistance("aaa", "aaaaa") == 2
assert sol.minDistance("kitten", "sitting") == 3
assert sol.minDistance("flaw", "lawn") == 2
