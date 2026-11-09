# REFERENCE: d510 EPI 16.3 Count the number of ways to traverse a 2D array
class Solution
  def number_of_ways(n: int, m: int) -> int
    if n < m
      n, m = m, n
    row = [1] * m
    for _ in 1..<n
      for j in 1..<m
        row[j] += row[j - 1]
    row[-1]
