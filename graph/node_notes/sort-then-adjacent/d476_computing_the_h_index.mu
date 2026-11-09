# REFERENCE: d476 EPI 13.3 Computing the h-index
class Solution
  def h_index(citations: [int]) -> int
    count for >i, c in sort(citations, reverse=true) if c > i
