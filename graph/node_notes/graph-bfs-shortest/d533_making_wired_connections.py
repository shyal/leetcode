# REFERENCE: d533 EPI 18.6 Making wired connections
class Solution:
    def is_any_placement_feasible(self, graph):
        side = [-1] * len(graph)
        for s in range(len(graph)):
            if side[s] != -1:
                continue
            side[s] = 0
            q = deque([s])
            while q:
                v = q.popleft()
                for w in graph[v]:
                    if side[w] == -1:
                        side[w] = 1 - side[v]
                        q.append(w)
                    elif side[w] == side[v]:
                        return False
        return True
