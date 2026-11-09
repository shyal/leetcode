# REFERENCE: d377 EPI 4.11 Rectangle intersection
class Solution:
    def intersect_rectangle(self, r1, r2):
        x, y = max(r1.x, r2.x), max(r1.y, r2.y)
        width = min(r1.x + r1.width, r2.x + r2.width) - x
        height = min(r1.y + r1.height, r2.y + r2.height) - y
        if width < 0 or height < 0:
            return Rect(0, 0, -1, -1)
        return Rect(x, y, width, height)
