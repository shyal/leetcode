# combo chain: two-sequence-align, problem 3 of 14. Run `make combos two-sequence-align` to see
# the chain and what is done today; the chain is saved in graph/chains/two-sequence-align.json.
"""
URL: https://leetcode.com/problems/delete-operation-for-two-strings/description/?envType=problem-list-v2&envId=vn57k9wr

583. Delete Operation for Two Strings

Given two strings word1 and word2, return the minimum number of steps required to make word1 and word2 the same.

In one step, you can delete exactly one character in either string.

Example 1:

Input: word1 = "sea", word2 = "eat"
Output: 2
Explanation: You need one step to make "sea" to "ea" and another step to make "eat" to "ea".

Example 2:

Input: word1 = "leetcode", word2 = "etco"
Output: 4

Constraints:

    1 <= word1.length, word2.length <= 500
    word1 and word2 consist of only lowercase English letters.

---

LEETCODE: Accepted (235 ms, 92.1 MB)
"""


class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        @cache
        def helper(a, b):
            if len(a) == 0 or len(b) == 0:
                return len(a) or len(b)
            if a[-1] == b[-1]:
                return helper(a[:-1], b[:-1])
            dela = helper(a[:-1], b)
            delb = helper(a, b[:-1])
            return min(dela, delb) + 1

        return helper(word1, word2)


sol = Solution()

print(sol.minDistance("sea", "eat"))  # 2

assert sol.minDistance("sea", "eat") == 2
assert sol.minDistance("leetcode", "etco") == 4

assert sol.minDistance("", "") == 0
assert sol.minDistance("a", "") == 1
assert sol.minDistance("", "a") == 1
assert sol.minDistance("a", "a") == 0
assert sol.minDistance("abc", "abc") == 0
assert sol.minDistance("abc", "def") == 6
assert sol.minDistance("aaaaa", "aaa") == 2
assert sol.minDistance("abcde", "ace") == 2
# assert sol.minDistance("a" * 500, "a" * 500) == 0
# assert sol.minDistance("a" * 500, "b" * 500) == 1000
# assert sol.minDistance("abcde" * 100, "edcba" * 100) == 602
# assert sol.minDistance("xyz" * 166 + "x", "zyx" * 166 + "y") == 334
