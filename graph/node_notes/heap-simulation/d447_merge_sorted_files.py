# REFERENCE: d447 EPI 10.1 Merge sorted files
class Solution:
    def merge_sorted_arrays(self, sorted_arrays):
        heap = [(a[0], i, 0) for i, a in enumerate(sorted_arrays) if a]
        heapify(heap)
        out = []
        while heap:
            x, i, j = heappop(heap)
            out.append(x)
            if j + 1 < len(sorted_arrays[i]):
                heappush(heap, (sorted_arrays[i][j + 1], i, j + 1))
        return out
