# REFERENCE: d185 Count Pairs
class Solution:
    def countPairs(self, xs, key, lookup):
        cnt = Counter()
        ans = 0
        for x in xs:
            ans += cnt[lookup(x)]
            cnt[key(x)] += 1
        return ans
