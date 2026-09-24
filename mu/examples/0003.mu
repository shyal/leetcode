# 3. Longest Substring Without Repeating Characters
def lengthOfLongestSubstring(s: str) -> int
  cnt = counter()
  lo = 0
  max from 0 for hi, c in s
    cnt[c] += 1
    while cnt[c] > 1
      cnt[s[lo]] -= 1
      lo += 1
    hi - lo + 1
