# REFERENCE: d531 EPI 18.4 Deadlock detection
class Solution:
    def is_deadlocked(self, graph):
        state = [0] * len(graph)

        def cycle_from(v):
            state[v] = 1
            for w in graph[v]:
                if state[w] == 1 or (state[w] == 0 and cycle_from(w)):
                    return True
            state[v] = 2
            return False

        return any(state[v] == 0 and cycle_from(v) for v in range(len(graph)))
