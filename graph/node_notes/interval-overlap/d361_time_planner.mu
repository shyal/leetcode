# REFERENCE: d361 Time Planner
class Solution
  def meeting_planner(slotsA: [[int]], slotsB: [[int]], dur: int) -> [int]
    ia, ib = 0
    while ia < len(slotsA) and ib < len(slotsB)
      start = max(slotsA[ia][0], slotsB[ib][0])
      end = min(slotsA[ia][1], slotsB[ib][1])
      if start + dur <= end
        return [start, start + dur]
      if slotsA[ia][1] < slotsB[ib][1]
        ia += 1
      else
        ib += 1
    []
