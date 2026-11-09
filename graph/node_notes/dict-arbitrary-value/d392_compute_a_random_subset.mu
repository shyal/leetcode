# REFERENCE: d392 EPI 5.15 Compute a random subset
class Solution
  def random_subset(n: int, k: int) -> [int]
    moved = {}
    for i in 0..<k
      j = randint(i, n - 1)
      moved[i], moved[j] = moved.get(j, j), moved.get(i, i)
    [moved[i] for i in 0..<k]
