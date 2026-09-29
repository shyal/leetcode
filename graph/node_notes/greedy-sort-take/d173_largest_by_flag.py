# REFERENCE: d173 Largest By Flag
class Solution:
    def largestByFlag(self, nums, flag):
        pools = {True: [], False: []}
        for x, f in zip(nums, flag):
            pools[f].append(x)
        pools[True].sort()
        pools[False].sort()
        return [pools[f].pop() for f in flag]
