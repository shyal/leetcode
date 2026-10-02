# REFERENCE: d183 Indices Of Each Character
class Solution:
    def indices(self, s):
        pos = defaultdict(list)
        for i, c in enumerate(s):
            pos[c].append(i)
        return pos
