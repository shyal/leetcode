# REFERENCE: d123 Boys Ratio Order
def byRatio(classes: [[int]]) -> [[int]]
  def ratio(b, s)
    b / s
  heap = [(ratio(b, s), b, s) for (b, s) in classes]
  heapify(heap)
  out = []
  while heap
    _, b, s = heappop(heap)
    out <- [b, s]
  out
