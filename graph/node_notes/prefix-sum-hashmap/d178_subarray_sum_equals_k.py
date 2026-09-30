# REFERENCE: d178 Subarray Sum Equals K
class Solution:
    def subarraySum(self, nums, k):
        D = defaultdict(int)
        D[0] = 1
        prefix = 0
        res = 0
        for n in nums:
            prefix += n
            if prefix - k in D:
                res += D[prefix - k]
            D[prefix] += 1
        return res
