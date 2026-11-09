# REFERENCE: d397 EPI 5.20 Compute rows in Pascal's Triangle
class Solution
  def generate_pascal_triangle(n: int) -> [[int]]
    ret rows = []
    for i in 0..<n
      row = [1] * (i + 1)
      for j in 1..<i
        row[j] = rows[-1][j - 1] + rows[-1][j]
      rows <- row
