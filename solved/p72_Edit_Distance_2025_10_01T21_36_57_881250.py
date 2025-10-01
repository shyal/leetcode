"""
URL: https://leetcode.com/problems/edit-distance/description/?envType=study-plan-v2&envId=leetcode-75

72. Edit Distance

Given two strings word1 and word2, return the minimum number of operations required to convert word1 to word2.

You have the following three operations permitted on a word:

        Insert a character
        Delete a character
        Replace a character


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

from functools import cache


class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        @cache
        def dp_str(a, b):
            if len(a) == 0 or len(b) == 0:
                return len(a) or len(b)
            if a[-1] == b[-1]:
                return dp_str(a[:-1], b[:-1])
            add = dp_str(a, b[:-1])
            rem = dp_str(a[:-1], b)
            sub = dp_str(a[:-1], b[:-1])
            return min(add, rem, sub) + 1

        @cache
        def dp(i, j):
            if i < 0:
                return j + 1
            if j < 0:
                return i + 1
            if word1[i] == word2[j]:
                return dp(i - 1, j - 1)
            add = dp(i, j - 1)
            rem = dp(i - 1, j)
            sub = dp(i - 1, j - 1)
            return min(add, rem, sub) + 1

        return dp(len(word1) - 1, len(word2) - 1)


sol = Solution()

assert sol.minDistance("saturday", "sunday") == 3
