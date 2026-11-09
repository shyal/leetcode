# REFERENCE: d509 EPI 16.2 Compute the Levenshtein distance
class Solution
  def levenshtein_distance(A: str, B: str) -> int
    prev = list(0..len(B))
    for i in 1..len(A)
      cur = [i]
      for j in 1..len(B)
        if A[i - 1] == B[j - 1]
          cur <- prev[j - 1]
        else
          cur <- 1 + min(prev[j - 1], prev[j], cur[j - 1])
      prev = cur
    prev[-1]
