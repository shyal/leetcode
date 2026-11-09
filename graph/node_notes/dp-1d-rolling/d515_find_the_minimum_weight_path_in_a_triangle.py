# REFERENCE: d515 EPI 16.8 Find the minimum weight path in a triangle
class Solution:
    def minimum_path_weight(self, triangle):
        if not triangle:
            return 0
        below = triangle[-1][:]
        for row in reversed(triangle[:-1]):
            below = [x + min(below[j], below[j + 1]) for j, x in enumerate(row)]
        return below[0]
