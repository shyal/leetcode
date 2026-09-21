# REFERENCE: d139 Node Step Pairs
class Solution:
    def reachable(self, G, k):
        seen = {(0, 0)}
        q = deque([0])
        for d, node in levels(q):
            for nxt in G[node]:
                if d < k and (nxt, d + 1) not in seen:
                    seen.add((nxt, d + 1))
                    q.append(nxt)
        return seen
