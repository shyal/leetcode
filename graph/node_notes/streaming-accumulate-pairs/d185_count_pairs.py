# REFERENCE: d185 Count Pairs
class Solution:
    def countPairs(self, xs, by, want):
        cnt = Counter()
        ans = 0
        for x in xs:
            ans += cnt[want(x)]
            cnt[by(x)] += 1
        return ans
