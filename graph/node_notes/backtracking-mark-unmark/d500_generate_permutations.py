# REFERENCE: d500 EPI 15.4 Generate permutations
class Solution:
    def permutations(self, A):
        out, perm = [], []
        used = [False] * len(A)

        def extend():
            if len(perm) == len(A):
                out.append(perm[:])
                return
            for i, x in enumerate(A):
                if not used[i]:
                    used[i] = True
                    perm.append(x)
                    extend()
                    perm.pop()
                    used[i] = False

        extend()
        return out
