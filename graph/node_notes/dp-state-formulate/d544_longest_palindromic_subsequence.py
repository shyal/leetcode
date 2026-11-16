# REFERENCE: d544 Longest Palindromic Subsequence
class Solution:
    def longestPalindromeSubseq(self, s):
        n = len(s)
        best = [[0] * n for _ in range(n)]
        for i in range(n - 1, -1, -1):
            best[i][i] = 1
            for j in range(i + 1, n):
                if s[i] == s[j]:
                    best[i][j] = 2 + best[i + 1][j - 1]
                else:
                    best[i][j] = max(best[i + 1][j], best[i][j - 1])
        return best[0][n - 1]
