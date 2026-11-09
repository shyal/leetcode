# REFERENCE: d470 EPI 12.8 Find the longest subarray with distinct entries
class Solution:
    def longest_subarray_with_distinct_entries(self, A):
        last, left, best = {}, 0, 0
        for i, x in enumerate(A):
            if last.get(x, -1) >= left:
                left = last[x] + 1
            last[x] = i
            best = max(best, i - left + 1)
        return best
