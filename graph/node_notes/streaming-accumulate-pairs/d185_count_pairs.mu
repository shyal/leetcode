# REFERENCE: d185 Count Pairs
class Solution
  def countPairs(xs: [int], key: int -> int, lookup: int -> int) -> int
    cnt = counter()
    sum for x in xs
      got = cnt[lookup(x)]
      cnt[key(x)] += 1
      got
