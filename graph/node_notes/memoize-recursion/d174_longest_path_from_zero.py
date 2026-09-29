# REFERENCE: d174 Longest Path From Zero
class Solution:
    def longestPath(self, G):
        @cache
        def longest(u):
            return max((1 + longest(v) for v in G[u]), default=0)

        return longest(0)
