# REFERENCE: d185 Count Pairs
def countPairs(xs: [int], by: int -> int, want: int -> int) -> int
  cnt = counter()
  sum for x in xs
    got = cnt[want(x)]
    cnt[by(x)] += 1
    got
