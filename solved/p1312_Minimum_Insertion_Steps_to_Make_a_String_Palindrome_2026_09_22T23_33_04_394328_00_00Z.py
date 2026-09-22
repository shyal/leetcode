# combo chain: two-sequence-align, problem 9 of 14. Run `make combos two-sequence-align` to see
# the chain and what is done today; the chain is saved in graph/chains/two-sequence-align.json.
"""
URL: https://leetcode.com/problems/minimum-insertion-steps-to-make-a-string-palindrome/description/?envType=problem-list-v2&envId=vn57k9wr

1312. Minimum Insertion Steps to Make a String Palindrome

Given a string s. In one step you can insert any character at any index of the string.

Return the minimum number of steps to make s palindrome.

A Palindrome String is one that reads the same backward as well as forward.

Example 1:

Input: s = "zzazz"
Output: 0
Explanation: The string "zzazz" is already palindrome we do not need any insertions.

Example 2:

Input: s = "mbadm"
Output: 2
Explanation: String can be "mbdadbm" or "mdbabdm".

Example 3:

Input: s = "leetcode"
Output: 5
Explanation: Inserting 5 characters the string becomes "leetcodocteel".

Constraints:

    1 <= s.length <= 500
    s consists of lowercase English letters.

---

LEETCODE: Accepted (2043 ms, 417.3 MB)
"""


class Solution:
    def minInsertions(self, s: str) -> int:
        @cache
        def mindist(a, b):
            if len(a) == 0 or len(b) == 0:
                return len(a) or len(b)
            if a[-1] == b[-1]:
                return mindist(a[:-1], b[:-1])
            dela = mindist(a[:-1], b)
            delb = mindist(a, b[:-1])
            return min([dela, delb]) + 1

        @cache
        def dp(i, j):
            if i < 0:
                return j + 1
            if j < 0:
                return i + 1
            if s[i] == s[::-1][j]:
                return dp(i - 1, j - 1)
            add = dp(i, j - 1)
            rem = dp(i - 1, j)
            return min(add, rem) + 1

        return dp(len(s) - 1, len(s) - 1) // 2
        # return mindist(s, s[::-1]) // 2


sol = Solution()

print(sol.minInsertions("mbadm"))  # 2

assert sol.minInsertions("zzazz") == 0
assert sol.minInsertions("mbadm") == 2
assert sol.minInsertions("leetcode") == 5

assert sol.minInsertions("a") == 0
assert sol.minInsertions("aa") == 0
assert sol.minInsertions("ab") == 1
assert sol.minInsertions("abcba") == 0
assert sol.minInsertions("abccba") == 0
assert sol.minInsertions("abcd") == 3
assert sol.minInsertions("aabbccddeeffgghh") == 14
assert sol.minInsertions("zyxwvutsrqponmlkjihgfedcbaabcdefghijklmnopqrstuvwxyz") == 0
assert sol.minInsertions("abcddcbaabcddcba") == 0
assert sol.minInsertions("abcddcbaabcddcbaz") == 1
