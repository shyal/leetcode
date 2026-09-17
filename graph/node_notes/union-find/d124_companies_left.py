# REFERENCE: d124 Companies Left
class Solution(UnionFind):
    def countCompanies(self):
        return sum(x == p for x, p in enumerate(self.parent))
