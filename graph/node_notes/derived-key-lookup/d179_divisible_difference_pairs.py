# REFERENCE: d179 Divisible Difference Pairs
class Solution:
    def divisiblePairs(self, nums, m):
        cnt = Counter()
        ans = 0
        for x in nums:
            ans += cnt[x % m]
            cnt[x % m] += 1
        return ans
