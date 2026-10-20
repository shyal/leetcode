# REFERENCE: d307 Minimum Path Cost
class Solution:
    def min_cost(self, G, s, t):
        cost, pq = {s: 0}, [(0, s)]
        while pq:
            c, u = heappop(pq)
            if u == t:
                return c
            for v, w in G[u].items():
                if c + w < cost.get(v, inf):
                    cost[v] = c + w
                    heappush(pq, (c + w, v))
        return -1
