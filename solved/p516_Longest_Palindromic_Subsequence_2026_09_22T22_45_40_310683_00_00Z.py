# combo chain: two-sequence-align, problem 8 of 14. Run `make combos two-sequence-align` to see
# the chain and what is done today; the chain is saved in graph/chains/two-sequence-align.json.
"""
URL: https://leetcode.com/problems/longest-palindromic-subsequence/description/?envType=problem-list-v2&envId=vn57k9wr

516. Longest Palindromic Subsequence

Given a string s, find the longest palindromic subsequence's length in s.

A subsequence is a sequence that can be derived from another sequence by deleting some or no elements without changing the order of the remaining elements.

Example 1:

Input: s = "bbbab"
Output: 4
Explanation: One possible longest palindromic subsequence is "bbbb".

Example 2:

Input: s = "cbbd"
Output: 2
Explanation: One possible longest palindromic subsequence is "bb".

Constraints:

    1 <= s.length <= 1000
    s consists only of lowercase English letters.

---

LEETCODE: Accepted (2705 ms, 405.1 MB)
"""


class Solution:
    def longestPalindromeSubseq(self, s: str) -> int:
        return len(lcs(s, s[::-1], type=str))


sol = Solution()

print(sol.longestPalindromeSubseq("bbbab"))  # 4

assert sol.longestPalindromeSubseq("bbbab") == 4
assert sol.longestPalindromeSubseq("cbbd") == 2

assert sol.longestPalindromeSubseq("a") == 1
assert sol.longestPalindromeSubseq("aa") == 2
assert sol.longestPalindromeSubseq("ab") == 1
assert sol.longestPalindromeSubseq("abcba") == 5
assert sol.longestPalindromeSubseq("abccba") == 6
assert sol.longestPalindromeSubseq("abcdedcba") == 9
assert sol.longestPalindromeSubseq("abcddcba") == 8
# assert sol.longestPalindromeSubseq("a" * 1000) == 1000
# assert sol.longestPalindromeSubseq("ab" * 500) == 999
# assert sol.longestPalindromeSubseq("abcde" * 200) == 399
# assert sol.longestPalindromeSubseq("z" * 999 + "y") == 999
# assert sol.longestPalindromeSubseq("a" * 499 + "b" + "a" * 500) == 999
