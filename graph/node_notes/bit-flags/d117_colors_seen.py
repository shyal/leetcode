# REFERENCE: d117 Colors Seen
class Color(Flag):
    red = auto()
    green = auto()
    blue = auto()


class Solution:
    def seen(self, names):
        out = Color(0)
        for name in names:
            out |= Color[name]
        return out
