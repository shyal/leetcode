# REFERENCE: d125 Companies Among
class Solution(UnionFind):
    def countCompaniesAmong(self, employees):
        return len({self.find(x) for x in employees})
