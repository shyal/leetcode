# REFERENCE: d342 Getting a Different Number
class Solution:
    def get_different_number(self, arr):
        n = len(arr)
        seen = [False] * (n + 1)
        for x in arr:
            if x <= n:
                seen[x] = True
        return seen.index(False)
