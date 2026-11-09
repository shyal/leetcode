# REFERENCE: d427 EPI 8.5 Compute buildings with a sunset view
class Solution
  def examine_buildings_with_sunset(sequence: Iterator[int]) -> [int]
    stack = []  # (index, height), heights strictly decreasing
    for >i, height in sequence
      while stack and stack[-1][1] <= height
        stack.pop()
      stack <- (i, height)
    [i for i, _ in reversed(stack)]
