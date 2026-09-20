# REFERENCE: d137 Subarrays Summing To Target
class Solution:
    def countSubarrays(self, vals, target):
        D = defaultdict(int)
        D[0] = 1
        prefix = res = 0
        for v in vals:
            prefix += v
            res += D[prefix - target]
            D[prefix] += 1
        return res
