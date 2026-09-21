# REFERENCE: d138 Exact Length Walks
class Solution:
    def exactWalks(self, n, edges, k):
        G = adjacency(edges, n=n)
        seen = {(0, 0)}
        q = deque([(0, 0)])
        out = []
        for d, (node, steps) in levels(q):
            if steps == k:
                out.append(node)
                continue
            for nxt in G[node]:
                item = (nxt, steps + 1)
                if item not in seen:
                    seen.add(item)
                    q.append(item)
        return out
