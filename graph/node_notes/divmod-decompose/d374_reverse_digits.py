# REFERENCE: d374 EPI 4.8 Reverse digits
class Solution:
    def reverse(self, x):
        out, rest = 0, abs(x)
        while rest:
            rest, d = divmod(rest, 10)
            out = out * 10 + d
        return out if x >= 0 else -out
