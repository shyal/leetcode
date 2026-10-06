# REFERENCE: d198 Lines Of A File
class Solution:
    def lines(self, path):
        with open(path) as f:
            return [line.rstrip("\n") for line in f]
