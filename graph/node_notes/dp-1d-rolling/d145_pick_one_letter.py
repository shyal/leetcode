# REFERENCE: d145 Pick One Letter
class Solution:
    def countPicks(self, s, c):
        ways = table(len(s) + 1, fill=0)
        for i in range(1, len(s) + 1):
            ways[i] = ways[i - 1]
            if s[i - 1] == c:
                ways[i] += 1
        return ways
