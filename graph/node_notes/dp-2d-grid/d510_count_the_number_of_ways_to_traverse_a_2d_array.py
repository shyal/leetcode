# REFERENCE: d510 EPI 16.3 Count the number of ways to traverse a 2D array
class Solution:
    def number_of_ways(self, n, m):
        if n < m:
            n, m = m, n
        row = [1] * m
        for _ in range(n - 1):
            for j in range(1, m):
                row[j] += row[j - 1]
        return row[-1]
