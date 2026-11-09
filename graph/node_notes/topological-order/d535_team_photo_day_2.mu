# REFERENCE: d535 EPI 18.8 Team photo day - 2
class Solution
  def find_largest_number_teams(graph: [[int]]) -> int
    indeg = table(len(graph))
    for edges in graph
      for w in edges
        indeg[w] += 1
    order = [v for v in 0..<len(graph) if indeg[v] == 0]
    longest = table(len(graph), fill=1)
    for v in order
      for w in graph[v]
        longest[w] = max(longest[w], longest[v] + 1)
        indeg[w] -= 1
        if indeg[w] == 0
          order <- w
    max longest
