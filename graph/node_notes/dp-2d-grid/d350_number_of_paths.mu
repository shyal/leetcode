# REFERENCE: d350 Number of Paths
class Solution
  def num_of_paths_to_dest(n: int) -> int
    paths = table(n, n, fill=0)
    paths[0][0] = 1
    for i in 0..<n
      for j in 0..i
        if i > 0
          paths[i][j] += paths[i - 1][j]
        if j > 0
          paths[i][j] += paths[i][j - 1]
    paths[n - 1][n - 1]
