# REFERENCE: d477 EPI 13.4 Remove first-name duplicates
class Solution:
    def eliminate_duplicate(self, A):
        A.sort()
        write = 0
        for name in A:
            if write == 0 or name[0] != A[write - 1][0]:
                A[write] = name
                write += 1
        del A[write:]
