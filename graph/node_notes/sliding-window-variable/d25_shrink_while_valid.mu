# REFERENCE: d25 Shrink While Valid
def shortestAtLeast(s: str, k: int) -> int
  count = defaultdict(int)
  best, left = inf, 0
  for right, v in s
    count[v] += 1
    while len(count) >= k
      best = min(best, right - left + 1)
      count[s[left]] -= 1
      if count[s[left]] == 0
        del count[s[left]]
      left += 1
  best if best < inf else 0
