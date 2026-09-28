# REFERENCE: d170 Plus One Or Double
class Solution:
    def fewest(self, a, b, limit):
        q = deque([a])
        for d, x in levels(q, seen=set(), lte=limit):  # values are the vertices
            if x == b:
                return d
            q += [x + 1, 2 * x]
        return -1
