# REFERENCE: d118 Names In Palette
class Solution:
    def present(self, palette, names):
        return [name for name in names if Color[name] in palette]
