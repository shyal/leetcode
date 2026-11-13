# URL: https://leetcode.com/problems/merge-intervals/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 56. Merge Intervals
#
# Given an array of intervals where intervals[i] = [start_i, end_i], merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.
#
# Example 1:
#
# Input: intervals = [[1,3],[2,6],[8,10],[15,18]]
# Output: [[1,6],[8,10],[15,18]]
# Explanation: Since intervals [1,3] and [2,6] overlap, merge them into [1,6].
#
# Example 2:
#
# Input: intervals = [[1,4],[4,5]]
# Output: [[1,5]]
# Explanation: Intervals [1,4] and [4,5] are considered overlapping.
#
# Example 3:
#
# Input: intervals = [[4,7],[1,4]]
# Output: [[1,7]]
# Explanation: Intervals [1,4] and [4,7] are considered overlapping.
#
# Constraints:
#
#     1 <= intervals.length <= 10^4
#     intervals[i].length == 2
#     0 <= start_i <= end_i <= 10^4
#
# ---
# STAGE 1 of 3 - the approach. Write it in plain English under this line. Then run make solved.
#
# sort by start then merge
# STAGE 1: pass
# STAGE 2 of 3 - the pseudocode. Write one comment line for each step in the solve below. Then run make solved.

# mu 0.17

class Solution
  def solve(x)
    # sort intervals by start
    # res = [first interval]
    # for each next interval
      # if its start <= end of the last in res
        # last end = max(last end, its end)
      # else
        # append it
    # return res
    pass

sol = Solution()
