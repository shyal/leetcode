# 435. Non-overlapping Intervals
def eraseOverlapIntervals(intervals: [(int, int)]) -> int
  end, kept = -inf, 0
  for (l, r) in sort(intervals, by=(_, r) -> r)
    if l >= end
      end, kept = r, kept + 1
  len(intervals) - kept
