# REFERENCE: d448 EPI 10.2 Sort an increasing-decreasing array
class Solution:
    def sort_k_increasing_decreasing_array(self, A):
        runs, start = [], 0
        for i in range(1, len(A) + 1):
            if i == len(A) or (i > start + 1 and (A[i - 1] < A[i]) != (A[start] < A[start + 1])):
                run = A[start:i]
                runs.append(run if run[0] <= run[-1] else run[::-1])
                start = i
        heap = [(run[0], r, 0) for r, run in enumerate(runs)]
        heapify(heap)
        out = []
        while heap:
            x, r, j = heappop(heap)
            out.append(x)
            if j + 1 < len(runs[r]):
                heappush(heap, (runs[r][j + 1], r, j + 1))
        return out
