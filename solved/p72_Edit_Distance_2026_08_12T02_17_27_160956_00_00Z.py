"""
URL: https://leetcode.com/problems/edit-distance/description/?envType=problem-list-v2&envId=vn57k9wr

72. Edit Distance

Given two strings word1 and word2, return the minimum number of operations
required to convert word1 to word2.

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

---
I prefered just peeking at my previous solves rather than struggling through
edit distance again. So this is a peek.

One clarification in my thinking is that previous i was using var names like
`add` and `del` without noticing they're symmetrical.

Technically they could also be called `adda` and `addb`. Add the last letter
of b only a, or adding the last letter of a onto be, are valid, just inefficient.

And this results in the same thing anyway, chopping off a letter from the end of a
or the end of b. So i've opted for dela and delb

Also this is the string version, which i'm happy with, once consolidated, i'll
go for the indices based version.
"""

class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        @cache
        def DP(a, b):
            if len(a) == 0 or len(b) == 0:
                return len(a) or len(b)
            if a[-1] == b[-1]:
                return DP(a[:-1], b[:-1])

            dela = DP(a[:-1], b)
            delb = DP(a, b[:-1])
            sub = DP(a[:-1], b[:-1])

            return min([delb, dela, sub]) + 1

        return DP(word1, word2)


sol = Solution()

# print(sol.minDistance("horse", "ros"))  # 3

assert sol.minDistance("horse", "ros") == 3
assert sol.minDistance("intention", "execution") == 5

assert sol.minDistance("", "") == 0
assert sol.minDistance("", "a") == 1
assert sol.minDistance("a", "") == 1
assert sol.minDistance("", "abcde") == 5
assert sol.minDistance("abc", "") == 3

assert sol.minDistance("a", "a") == 0
assert sol.minDistance("a", "b") == 1
assert sol.minDistance("abcde", "abcde") == 0

assert sol.minDistance("abcde", "abc") == 2
assert sol.minDistance("abc", "abcde") == 2
assert sol.minDistance("bcd", "abcde") == 2
assert sol.minDistance("ace", "abcde") == 2
assert sol.minDistance("islander", "slander") == 1

assert sol.minDistance("abc", "xyz") == 3
assert sol.minDistance("abcd", "xy") == 4
assert sol.minDistance("xy", "abcd") == 4

assert sol.minDistance("ab", "ba") == 2
assert sol.minDistance("abab", "baba") == 2
assert sol.minDistance("ababab", "bababa") == 2

assert sol.minDistance("aaa", "aa") == 1
assert sol.minDistance("aaa", "aaaa") == 1
assert sol.minDistance("a", "aaa") == 2
assert sol.minDistance("aaaa", "a") == 3

assert sol.minDistance("kitten", "sitting") == 3
assert sol.minDistance("sunday", "saturday") == 3
assert sol.minDistance("mart", "karma") == 3
assert sol.minDistance("park", "spake") == 3
assert sol.minDistance("abcdef", "azced") == 3
assert sol.minDistance("abc", "yabd") == 2
assert sol.minDistance("distance", "instance") == 2

assert sol.minDistance("ros", "horse") == 3
assert sol.minDistance("execution", "intention") == 5
assert sol.minDistance("saturday", "sunday") == 3
assert sol.minDistance("karma", "mart") == 3

# assert sol.minDistance("a" * 500, "") == 500
# assert sol.minDistance("", "b" * 500) == 500
# assert sol.minDistance("a" * 500, "a" * 500) == 0
# assert sol.minDistance("a" * 500, "b" * 500) == 500
# assert sol.minDistance("a" * 500, "a" * 499 + "b") == 1
# assert sol.minDistance("a" * 500, "a" * 250) == 250