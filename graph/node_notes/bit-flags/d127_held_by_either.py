# REFERENCE: d127 Held By Either
class Solution:
    def either(self, a, b, names):
        return [name for name in names if Color[name] in a | b]
