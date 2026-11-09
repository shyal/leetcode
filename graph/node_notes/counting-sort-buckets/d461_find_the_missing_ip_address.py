# REFERENCE: d461 EPI 11.9 Find the missing IP address
class Solution:
    def find_missing_element(self, stream):
        size = 1 << 16
        counts = [0] * size
        for v in stream:
            counts[v >> 16] += 1
        high = next(i for i, c in enumerate(counts) if c < size)
        seen = [False] * size
        for v in stream:
            if v >> 16 == high:
                seen[v & (size - 1)] = True
        return high << 16 | seen.index(False)
