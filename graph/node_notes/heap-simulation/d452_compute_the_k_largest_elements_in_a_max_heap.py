# REFERENCE: d452 EPI 10.6 Compute the k largest elements in a max-heap
class Solution:
    def k_largest_in_binary_heap(self, A, k):
        out, cand = [], [(A[0], 0)]
        while len(out) < k:
            x, i = maxheappop(cand)
            out.append(x)
            for c in (2 * i + 1, 2 * i + 2):
                if c < len(A):
                    maxheappush(cand, (A[c], c))
        return out
