# REFERENCE: d449 EPI 10.3 Sort an almost-sorted array
class Solution:
    def sort_approximately_sorted_array(self, sequence, k):
        heap = list(islice(sequence, k))
        heapify(heap)
        out = [heapq.heappushpop(heap, x) for x in sequence]
        while heap:
            out.append(heappop(heap))
        return out
