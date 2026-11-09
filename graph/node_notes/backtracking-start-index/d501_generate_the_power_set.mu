# REFERENCE: d501 EPI 15.5 Generate the power set
class Solution
  def generate_power_set(input_set: [int]) -> [[int]]
    ret out, subset = []..
    def grow(start)
      out <- subset[:]
      for i in start..<len(input_set)
        subset <- input_set[i]
        grow(i + 1)
        subset .
    grow(0)
