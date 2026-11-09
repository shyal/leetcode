# REFERENCE: d462 EPI 11.10 Find the duplicate and missing elements
class Solution:
    def find_duplicate_missing(self, A):
        both = 0
        for i, a in enumerate(A):
            both ^= i ^ a
        bit = both & -both
        x = 0
        for i, a in enumerate(A):
            if i & bit:
                x ^= i
            if a & bit:
                x ^= a
        return (x, x ^ both) if x in A else (x ^ both, x)
