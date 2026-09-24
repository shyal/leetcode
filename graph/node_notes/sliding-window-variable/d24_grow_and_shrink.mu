# REFERENCE: d24 Grow and Shrink
def longestAtMost(s: str, k: int) -> int
  count = defaultdict(int)
  left = 0
  max from 0 for right, v in s
    count[v] += 1
    while len(count) > k
      count[s[left]] -= 1
      if count[s[left]] == 0
        del count[s[left]]
      left += 1
    right - left + 1
