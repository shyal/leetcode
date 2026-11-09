# REFERENCE: d492 EPI 14.7 Enumerate extended integers
class Solution
  def generate_first_k_a_b_sqrt2(k: int) -> [float]
    def value(p): p[0] + p[1] * sqrt(2)
    pairs, i, j = [(0, 0)], 0, 0
    while len(pairs) < k
      plus_one = (pairs[i][0] + 1, pairs[i][1])
      plus_root = (pairs[j][0], pairs[j][1] + 1)
      nxt = min(plus_one, plus_root, key=value)
      pairs <- nxt
      i += plus_one == nxt
      j += plus_root == nxt
    [value(p) for p in pairs[:k]]
