# REFERENCE: d393 EPI 5.16 Generate nonuniform random numbers
class Solution
  def nonuniform_random_number_generation(values: [int], probabilities: [float]) -> int
    ends = list(accumulate(probabilities))
    i = bisect.bisect_right(ends, random.random() * ends[-1])
    values[min(i, len(values) - 1)]
