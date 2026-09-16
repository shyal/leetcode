# REFERENCE: d123 Boys Ratio Order
class Solution:
    def byRatio(self, classes):
        def ratio(b, s):
            return b / s

        heap = [(ratio(b, s), b, s) for b, s in classes]
        heapify(heap)
        out = []
        while heap:
            _, b, s = heappop(heap)
            out.append([b, s])
        return out
