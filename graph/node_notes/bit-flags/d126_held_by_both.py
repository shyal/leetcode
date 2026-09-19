# REFERENCE: d126 Held By Both
class Solution:
    def both(self, a, b, names):
        return [name for name in names if Color[name] in a & b]
