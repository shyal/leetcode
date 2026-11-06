# REFERENCE: d333 Busiest Time in The Mall
class Solution
  def find_busiest_period(data: [[int]]) -> int
    count, best_time = 0
    best = -inf
    for >i, (time, visitors, entered) in data
      count += entered ? visitors : -visitors
      if i + 1 < len(data) and data[i + 1][0] == time
        continue
      if count > best
        best, best_time = count, time
    best_time
