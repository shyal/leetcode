# REFERENCE: d397 EPI 5.20 Compute rows in Pascal's Triangle
class Solution:
    def generate_pascal_triangle(self, n):
        rows = []
        for i in range(n):
            row = [1] * (i + 1)
            for j in range(1, i):
                row[j] = rows[-1][j - 1] + rows[-1][j]
            rows.append(row)
        return rows
