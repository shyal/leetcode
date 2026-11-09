# REFERENCE: d535 EPI 18.8 Team photo day - 2
class Solution:
    def find_largest_number_teams(self, graph):
        indeg = [0] * len(graph)
        for edges in graph:
            for w in edges:
                indeg[w] += 1
        order = [v for v in range(len(graph)) if indeg[v] == 0]
        longest = [1] * len(graph)
        for v in order:
            for w in graph[v]:
                longest[w] = max(longest[w], longest[v] + 1)
                indeg[w] -= 1
                if indeg[w] == 0:
                    order.append(w)
        return max(longest)
