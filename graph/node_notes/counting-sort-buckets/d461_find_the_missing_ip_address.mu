# REFERENCE: d461 EPI 11.9 Find the missing IP address
class Solution
  def find_missing_element(stream: [int]) -> int
    size = 1 << 16
    counts = [0] * size
    for v in stream
      counts[v >> 16] += 1
    high = next(i for i, c in enumerate(counts) if c < size)
    seen = [false] * size
    for v in stream
      if v >> 16 == high
        seen[v & (size - 1)] = true
    high << 16 | seen.index(false)
