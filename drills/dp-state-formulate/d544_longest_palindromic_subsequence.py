"""
Given a string s, find the longest palindromic subsequence's length in s.

A subsequence is a sequence that can be derived from another sequence by
deleting some or no elements without changing the order of the remaining
elements.

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

    REQUIRED: O(n^2) time.
"""


class Solution:
    def longestPalindromeSubseq(self, s: str) -> int:
        pass


sol = Solution()

print(sol.longestPalindromeSubseq("bbbab"))  # 4

# assert sol.longestPalindromeSubseq("bbbab") == 4
# assert sol.longestPalindromeSubseq("cbbd") == 2
# assert sol.longestPalindromeSubseq("a") == 1
# assert sol.longestPalindromeSubseq("aa") == 2
# assert sol.longestPalindromeSubseq("ab") == 1
# assert sol.longestPalindromeSubseq("aba") == 3
# assert sol.longestPalindromeSubseq("abc") == 1
# assert sol.longestPalindromeSubseq("abca") == 3
# assert sol.longestPalindromeSubseq("abcba") == 5
# assert sol.longestPalindromeSubseq("abcabc") == 3
# assert sol.longestPalindromeSubseq("aabb") == 2
# assert sol.longestPalindromeSubseq("racecar") == 7
# assert sol.longestPalindromeSubseq("character") == 5
# assert sol.longestPalindromeSubseq("agbdba") == 5
# assert sol.longestPalindromeSubseq("abacdfgdcaba") == 11
# assert sol.longestPalindromeSubseq("a" * 1000) == 1000
# assert sol.longestPalindromeSubseq("ab" * 500) == 999
# assert sol.longestPalindromeSubseq("abcdefghij" * 100) == 199
