# REFERENCE: d177 Cut To K
class Solution:
    def cutToK(self, chunks, k):
        while len(chunks) < k:
            for i, c in enumerate(chunks):
                if len(c) > 1:
                    chunks[i : i + 1] = [[c[0]], c[1:]]
                    break
        return chunks
