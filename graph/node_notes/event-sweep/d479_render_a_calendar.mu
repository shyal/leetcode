# REFERENCE: d479 EPI 13.6 Render a calendar
class Solution
  def find_max_simultaneous_events(A: [(int, int)]) -> int
    events = sort([(s, 0) for s, _ in A] + [(f, 1) for _, f in A])
    ret best = 0
    count = 0
    for _, is_finish in events
      count += is_finish ? -1 : 1
      best = max(best, count)
