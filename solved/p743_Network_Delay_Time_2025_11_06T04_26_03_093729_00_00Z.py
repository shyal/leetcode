"""
URL: https://leetcode.com/problems/network-delay-time/description/?envType=problem-list-v2&envId=vn57k9wr

743. Network Delay Time

You are given a network of n nodes, labeled from 1 to n. You are also given times, a list of travel times as directed edges times[i] = (u_i, v_i, w_i), where u_i is the source node, v_i is the target node, and w_i is the time it takes for a signal to travel from source to target.

We will send a signal from a given node k. Return the minimum time it takes for all the n nodes to receive the signal. If it is impossible for all the n nodes to receive the signal, return -1.

Example 1:

Input: times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2
Output: 2

Example 2:

Input: times = [[1,2,1]], n = 2, k = 1
Output: 1

Example 3:

Input: times = [[1,2,1]], n = 2, k = 2
Output: -1

Constraints:

    1 <= k <= n <= 100
    1 <= times.length <= 6000
    times[i].length == 3
    1 <= u_i, v_i <= n
    u_i != v_i
    0 <= w_i <= 100
    All the pairs (u_i, v_i) are unique. (i.e., no multiple edges.)
"""


class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        graph = defaultdict(dict)

        for i in range(1, n + 1):
            graph[i]

        for source, target, time in times:
            graph[source][target] = time

        draw_graphviz(graph)

        dist = [maxsize] * (n + 1)
        dist[k] = 0

        pq = [(0, k)]

        while pq:
            d, u = heappop(pq)
            if d > dist[u]:
                continue
            for v, w in graph[u].items():
                if dist[v] > dist[u] + w:
                    dist[v] = dist[u] + w
                    heappush(pq, (dist[v], v))

        max_dist = max(dist[1:])
        return max_dist if max_dist != maxsize else -1


sol = Solution()

# print(sol.networkDelayTime([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2))  # 2

assert sol.networkDelayTime([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2) == 2
assert sol.networkDelayTime([[1, 2, 1]], 2, 1) == 1
assert sol.networkDelayTime([[1, 2, 1]], 2, 2) == -1
assert sol.networkDelayTime([], 1, 1) == 0
assert sol.networkDelayTime([], 2, 1) == -1
assert sol.networkDelayTime([[1, 2, 0]], 2, 1) == 0
assert sol.networkDelayTime([[1, 2, 1], [2, 3, 2], [3, 4, 3]], 4, 1) == 6
assert sol.networkDelayTime([[1, 3, 10], [1, 2, 1], [2, 3, 1]], 3, 1) == 2
assert sol.networkDelayTime([[1, 2, 1], [2, 1, 1]], 2, 1) == 1
assert sol.networkDelayTime([[1, 2, 1], [3, 4, 1]], 4, 3) == -1
assert sol.networkDelayTime([[1, 2, 100], [2, 3, 100], [1, 3, 100]], 3, 1) == 100
assert sol.networkDelayTime([[2, 1, 1], [3, 1, 1], [4, 1, 1]], 4, 1) == -1
assert sol.networkDelayTime([[1, 2, 1], [2, 3, 1], [3, 1, 1]], 3, 1) == 2
