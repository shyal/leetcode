# REFERENCE: d449 EPI 10.3 Sort an almost-sorted array
class Solution
  def sort_approximately_sorted_array(sequence: Iterator[int], k: int) -> [int]
    h = heap(islice(sequence, k))
    out = []
    for x in sequence
      h <- x
      out <- h .
    while h
      out <- h .
    out
