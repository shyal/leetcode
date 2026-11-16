# REFERENCE: d546 Earliest Indices Of A Subsequence
class Solution:
    def earliest_indices(self, sub, s):
        j = -1
        res = []
        for c in sub:
            j = s.index(c, j + 1)
            res.append(j)
        return res
