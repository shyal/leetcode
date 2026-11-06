# REFERENCE: d344 K-Messed Array Sort
class Solution:
    def sort_k_messed_array(self, arr, k):
        heap = arr[: k + 1]
        heapify(heap)
        out = []
        for x in arr[k + 1 :]:
            out.append(heappop(heap))
            heappush(heap, x)
        while heap:
            out.append(heappop(heap))
        return out
