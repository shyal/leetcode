"""
DRILL: Longest Common Subsequence

Given two strings a and b, return the length of the longest string that is
a subsequence of both. A subsequence is what is left after deleting zero or
more characters from a string, with the order of the rest unchanged.

Example 1:

Input: a = "abcde", b = "ace"
Output: 3
Explanation: "ace" is a subsequence of both.

Example 2:

Input: a = "abc", b = "def"
Output: 0

Example 3:

Input: a = "abc", b = "cba"
Output: 1
Explanation: order is kept, so a common subsequence of length 2 would have
to appear in the same direction in both. Only single characters do.

Constraints:

    1 <= len(a), len(b) <= 1000
    a and b consist of lowercase English letters.

    REQUIRED: O(len(a) * len(b)) time. Enumerating the subsequences of a
    and testing each one against b is exponential, the failure mode this
    drill exists to kill. NO itertools.
"""


class Solution:
    def lcs(self, a: str, b: str) -> int:
        pass


sol = Solution()

print(sol.lcs("abcde", "ace"))  # 3

# assert sol.lcs("abcde", "ace") == 3
# assert sol.lcs("abc", "def") == 0
# assert sol.lcs("abc", "cba") == 1
# assert sol.lcs("abc", "abc") == 3
# assert sol.lcs("a", "a") == 1
# assert sol.lcs("a", "b") == 0
# assert sol.lcs("aa", "a") == 1
# assert sol.lcs("aaa", "aa") == 2
# assert sol.lcs("bsbininm", "jmjkbkjkv") == 1
# assert sol.lcs("oxcpqrsvwf", "shmtulqrypy") == 2
# assert sol.lcs("ezupkr", "ubmrapg") == 2
# assert sol.lcs("a" * 1000, "a" * 1000) == 1000
