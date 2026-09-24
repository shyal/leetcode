# REFERENCE: d146 Count AB Subsequences
def countAB(s: str) -> int
  a, ab = 0, 0
  for ch in s
    if ch == "b"
      ab += a
    if ch == "a"
      a += 1
  ab
