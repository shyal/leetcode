# REFERENCE: d344 K-Messed Array Sort
class Solution
  def sort_k_messed_array(arr: [int], k: int) -> [int]
    h = heap(arr[:k + 1])
    out = []
    for x in arr[k + 1:]
      out <- h.pop()
      h.push(x)
    while h
      out <- h.pop()
    out
