# REFERENCE: d22 Fixed Slide
def maxDistinct(s: str, k: int) -> int
  count = defaultdict(int)
  max from 0 for i, v in s
    count[v] += 1
    if i >= k
      count[s[i - k]] -= 1
      if count[s[i - k]] == 0
        del count[s[i - k]]
    len(count)
