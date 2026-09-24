# REFERENCE: d145 Pick One Letter
def countPicks(s: str, c: str) -> [int]
  ways = table(len(s) + 1, fill = 0)
  for i in 1..len(s)
    ways[i] = ways[i - 1]
    if s[i - 1] == c
      ways[i] += 1
  ways
