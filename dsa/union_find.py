class UnionFind:
    def __init__(self, n):
        self.parent = [*range(n)]

    def find(self, x):
        while self.parent[x] != x:
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        self.parent[ra] = rb
        return True

    def groups(self):
        g = defaultdict(list)
        for x in range(len(self.parent)):
            g[self.find(x)].append(x)
        return g

    def union_shared(self, items):
        owner = {}
        for x, keys in enumerate(items):
            for key in keys:
                if key in owner:
                    self.union(x, owner[key])
                else:
                    owner[key] = x
