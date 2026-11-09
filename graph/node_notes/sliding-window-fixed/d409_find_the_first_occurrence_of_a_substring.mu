# REFERENCE: d409 EPI 6.12 Find the first occurrence of a substring
class Solution
  def rabin_karp(t: str, s: str) -> int
    m, n = len(t), len(s)
    BASE, MOD = 256, (1 << 61) - 1
    power = pow(BASE, max(n - 1, 0), MOD)
    hs = ht = 0
    for i in 0..<min(n, m)
      hs = (hs * BASE + ord(s[i])) % MOD
      ht = (ht * BASE + ord(t[i])) % MOD
    for i in 0..<m - n + 1
      if ht == hs and t[i:i + n] == s
        return i
      if i + n < m
        ht = ((ht - ord(t[i]) * power) * BASE + ord(t[i + n])) % MOD
    -1
