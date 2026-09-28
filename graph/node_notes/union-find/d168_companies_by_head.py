# REFERENCE: d168 Companies By Head
class Solution(UnionFind):
    def groups(self):
        g = defaultdict(list)
        for x in range(len(self.parent)):
            g[self.find(x)].append(x)
        return g
