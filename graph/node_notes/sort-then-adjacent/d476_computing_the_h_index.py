# REFERENCE: d476 EPI 13.3 Computing the h-index
class Solution:
    def h_index(self, citations):
        return sum(c > i for i, c in enumerate(sorted(citations, reverse=True)))
