# REFERENCE: d146 Count AB Subsequences
class Solution:
    def countAB(self, s):
        a = ab = 0
        for ch in s:
            if ch == "b":
                ab += a
            if ch == "a":
                a += 1
        return ab
