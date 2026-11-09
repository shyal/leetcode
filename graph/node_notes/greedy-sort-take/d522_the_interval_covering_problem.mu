# REFERENCE: d522 EPI 17.3 The interval covering problem
class Solution
  def find_minimum_visits(intervals: [[int]]) -> int
    ret visits, last = 0, -1
    for left, right in sort(intervals, by=iv -> iv[1])
      if left > last
        visits, last = visits + 1, right
