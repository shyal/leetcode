# REFERENCE: d532 EPI 18.5 Clone a graph
class Solution:
    def clone_graph(self, graph):
        copy = {graph: GraphNode(graph.val)}
        q = deque([graph])
        while q:
            v = q.popleft()
            for w in v.neighbors:
                if w not in copy:
                    copy[w] = GraphNode(w.val)
                    q.append(w)
                copy[v].neighbors.append(copy[w])
        return copy[graph]
