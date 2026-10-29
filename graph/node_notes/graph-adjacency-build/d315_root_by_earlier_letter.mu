# REFERENCE: d315 Root By Earlier Letter
class Solution
  def findRoot(n: int, edges: [[int]], letters: str) -> int
    child = [false] * n  # true at the child end of every edge
    for a, b in edges
      child[a if letters[a] > letters[b] else b] = true
    return child.index(false)
