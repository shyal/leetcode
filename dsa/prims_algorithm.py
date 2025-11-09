class Solution:

    def minCostConnectPoints(self, p: List[List[int]]) -> int:
        N = len(p)
        if N <= 1:
            return 0

        G = defaultdict(dict)
        for i in range(N):
            for j in range(i + 1, N):
                x_i, y_i = p[i]
                x_j, y_j = p[j]
                dist = abs(x_i - x_j) + abs(y_i - y_j)
                G[i][j] = dist
                G[j][i] = dist

        draw_graphviz(G, show_weights=True)

        visited = set()
        min_dist = [float("inf")] * N
        min_dist[0] = 0
        pq = [(0, 0)]

        while pq:
            _, a = heappop(pq)
            if a in visited:
                continue
            visited.add(a)
            for b in set(G[a]) - visited:
                if G[a][b] < min_dist[b]:
                    min_dist[b] = G[a][b]
                    heappush(pq, (min_dist[b], b))

        return sum(min_dist)


sol = Solution()

sol.minCostConnectPoints([[0, 0], [2, 2], [3, 10]])

assert sol.minCostConnectPoints([[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]) == 20
assert sol.minCostConnectPoints([[3, 12], [-2, 5], [-4, 1]]) == 18
assert sol.minCostConnectPoints([]) == 0
assert sol.minCostConnectPoints([[5, 5]]) == 0
assert sol.minCostConnectPoints([[0, 0], [1, 1]]) == 2
assert sol.minCostConnectPoints([[0, 0], [0, 1], [0, 2]]) == 2
assert sol.minCostConnectPoints([[1, 1], [2, 2], [3, 3], [4, 4]]) == 6
assert sol.minCostConnectPoints([[0, 0], [3, 0], [0, 4]]) == 7
assert sol.minCostConnectPoints([[-1000000, -1000000], [1000000, 1000000]]) == 4000000
