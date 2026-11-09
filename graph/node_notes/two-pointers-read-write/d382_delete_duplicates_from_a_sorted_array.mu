# REFERENCE: d382 EPI 5.5 Delete duplicates from a sorted array
class Solution
  def delete_duplicates(A: [int]) -> int
    w = 0
    for x in A
      if w == 0 or A[w - 1] != x
        A[w] = x
        w += 1
    w
