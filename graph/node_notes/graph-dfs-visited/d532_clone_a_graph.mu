# REFERENCE: d532 EPI 18.5 Clone a graph
class Solution
  def clone_graph(graph: GraphNode) -> GraphNode
    copy = {graph: GraphNode(graph.val)}
    q = deque([graph])
    while q
      v = q.popleft()
      for w in v.neighbors
        if w not in copy
          copy[w] = GraphNode(w.val)
          q <- w
        copy[v].neighbors <- copy[w]
    copy[graph]
