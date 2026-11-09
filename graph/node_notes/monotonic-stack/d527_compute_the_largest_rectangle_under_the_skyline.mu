# REFERENCE: d527 EPI 17.8 Compute the largest rectangle under the skyline
class Solution
  def calculate_largest_rectangle(heights: [int]) -> int
    stack = []
    ret best = 0
    for >i, h in heights + [0]
      while stack and heights[stack[-1]] >= h
        top = heights[stack .]
        width = stack ? i - stack[-1] - 1 : i
        best = max(best, top * width)
      stack <- i
