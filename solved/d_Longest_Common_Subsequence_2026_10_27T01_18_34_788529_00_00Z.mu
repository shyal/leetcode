# Given two strings a and b, return the length of the longest string that is
# a subsequence of both. A subsequence is what is left after deleting zero or
# more characters from a string, with the order of the rest unchanged.
#
# Example 1:
#
# Input: a = "abcde", b = "ace"
# Output: 3
# Explanation: "ace" is a subsequence of both.
#
# Example 2:
#
# Input: a = "abc", b = "def"
# Output: 0
#
# Example 3:
#
# Input: a = "abc", b = "cba"
# Output: 1
# Explanation: the order does not change, so a common subsequence of length 2 would have
# to appear in the same direction in both. Only single characters do.
#
# Constraints:
#
#     1 <= len(a), len(b) <= 1000
#     a and b consist of lowercase English letters.
#
#     REQUIRED: O(len(a) * len(b)) time. Enumerating the subsequences of a
#     and testing each one against b is exponential, the failure mode this
#     drill exists to kill. NO itertools.
#
# ---

# mu 0.13

class Solution
  def lcs(a: str, b: str) -> int
    a, b = f' {a}', f' {b}'
    dp = table(len(a), len(b))
    for i in 1..<len(a)
      for j in 1..<len(b)
        if a[i] == b[j]
          dp[i][j] = dp[i-1][j-1] + 1
        else
          dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    dp[-1][-1]

sol = Solution()

print(sol.lcs('abcde', 'ace'))  # 3

assert sol.lcs('abcde', 'ace') == 3
assert sol.lcs('abc', 'def') == 0
assert sol.lcs('abc', 'cba') == 1
assert sol.lcs('abc', 'abc') == 3
assert sol.lcs('a', 'a') == 1
assert sol.lcs('a', 'b') == 0
assert sol.lcs('aa', 'a') == 1
assert sol.lcs('aaa', 'aa') == 2
assert sol.lcs('bsbininm', 'jmjkbkjkv') == 1
assert sol.lcs('oxcpqrsvwf', 'shmtulqrypy') == 2
assert sol.lcs('ezupkr', 'ubmrapg') == 2
assert sol.lcs('a' * 1000, 'a' * 1000) == 1000
