# REFERENCE: d155 Equal Pairs
class Solution:
    def equalPairs(self, nums):
        cnt = Counter()
        ans = 0
        for x in nums:
            ans += cnt[x]
            cnt[x] += 1
        return ans
