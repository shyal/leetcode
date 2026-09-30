# REFERENCE: d177 Cut To K
class Solution:
    def cutToK(self, chunks, k):
        out = [list(c) for c in chunks]
        while len(out) < k:
            for i, c in enumerate(out):
                if len(c) > 1:
                    out[i : i + 1] = [[c[0]], c[1:]]
                    break
        return out
