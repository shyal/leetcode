# REFERENCE: d491 EPI 14.6 Find the closest entries in three sorted arrays
class Solution
  def find_closest_elements_in_sorted_arrays(sorted_arrays: [[int]]) -> int
    heap = [(a[0], i, 0) for i, a in enumerate(sorted_arrays)]
    heapify(heap)
    top = max(a[0] for a in sorted_arrays)
    best = inf
    while true
      low, i, j = heappop(heap)
      best = min(best, top - low)
      if j + 1 == len(sorted_arrays[i])
        return best
      nxt = sorted_arrays[i][j + 1]
      top = max(top, nxt)
      heappush(heap, (nxt, i, j + 1))
