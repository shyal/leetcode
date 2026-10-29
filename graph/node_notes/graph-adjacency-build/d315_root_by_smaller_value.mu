# REFERENCE: d315 Root By Smaller Value
class Solution
  def findRoot(edges: [[int]], values: [int]) -> int
    child = set()  # the child end of every edge: the end with the larger value
    for a, b in edges
      if values[a] == values[b]
        return -1
      child.add(values[a] < values[b] ? b : a)
    if len(child) != len(edges)  # a node that is the child end twice
      return -1
    [i for i in 0..<len(values) if i not in child][0]
