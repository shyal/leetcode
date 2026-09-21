# REFERENCE: d138 Even Length Walks
class Solution:
    def evenWalks(self, n, edges):
        G = adjacency(edges, n=n)
        ans = table(n, fill=-1)
        seen = {(0, 0)}
        q = deque([(0, 0)])
        d = 0
        while q:
            for _ in range(len(q)):
                node, parity = q.popleft()
                if parity == 0 and ans[node] == -1:
                    ans[node] = d
                for nxt in G[node]:
                    if (nxt, 1 - parity) not in seen:
                        seen.add((nxt, 1 - parity))
                        q.append((nxt, 1 - parity))
            d += 1
        return ans
