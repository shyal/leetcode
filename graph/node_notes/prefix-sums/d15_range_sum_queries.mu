# REFERENCE: d15 Range Sum Queries
class Solution
  def rangeSums(nums: [int], queries: [(int, int)]) -> [int]
    pre = [0, *scan(+, nums)]
    [pre[r + 1] - pre[l] for (l, r) in queries]
