"""
URL: https://leetcode.com/problems/non-overlapping-intervals/description/?envType=study-plan-v2&envId=leetcode-75

435. Non-overlapping Intervals

Given an array of intervals intervals where intervals[i] = [starti, endi], return the minimum number of intervals you need to remove to make the rest of the intervals non-overlapping.

Note that intervals which only touch at a point are non-overlapping. For example, [1, 2] and [2, 3] are non-overlapping.


Example 1:

Input: intervals = [[1,2],[2,3],[3,4],[1,3]]
Output: 1
Explanation: [1,3] can be removed and the rest of the intervals are non-overlapping.

Example 2:

Input: intervals = [[1,2],[1,2],[1,2]]
Output: 2
Explanation: You need to remove two [1,2] to make the rest of the intervals non-overlapping.

Example 3:

Input: intervals = [[1,2],[2,3]]
Output: 0
Explanation: You don't need to remove any of the intervals since they're already non-overlapping.


Constraints:

        1 <= intervals.length <= 105
        intervals[i].length == 2
        -5 * 104 <= starti < endi <= 5 * 104
"""

from typing import List


class Solution:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        intervals.sort(key=lambda x: x[1])
        prev = intervals[0]
        count = 1
        for interval in intervals:
            overlap = interval[0] < prev[1]
            if not overlap:
                prev = interval
                count += 1
        return len(intervals) - count


sol = Solution()

res = sol.eraseOverlapIntervals(intervals=[[1, 2], [2, 3], [3, 4], [1, 3]])
assert res == 1

res = sol.eraseOverlapIntervals(
    intervals=[[0, 2], [1, 3], [1, 3], [2, 4], [3, 5], [3, 5], [4, 6]]
)
assert res == 4

res = sol.eraseOverlapIntervals(intervals=[[1, 2], [1, 2], [1, 2]])
assert res == 2

res = sol.eraseOverlapIntervals(intervals=[[1, 2], [2, 3]])
assert res == 0

res = sol.eraseOverlapIntervals(intervals=[[1, 2]])
assert res == 0

res = sol.eraseOverlapIntervals(intervals=[[1, 5], [3, 6], [5, 7]])
assert res == 1

res = sol.eraseOverlapIntervals(intervals=[[-10, -5], [-4, 0], [1, 2]])
assert res == 0

res = sol.eraseOverlapIntervals(intervals=[[1, 10], [2, 3], [3, 4], [4, 5], [5, 6]])
assert res == 1

res = sol.eraseOverlapIntervals(intervals=[[1, 2], [1, 3]])
assert res == 1

res = sol.eraseOverlapIntervals(intervals=[[0, 2], [1, 3], [2, 4], [3, 5], [4, 6]])
assert res == 2

res = sol.eraseOverlapIntervals(intervals=[[1, 2], [1, 2], [1, 2], [1, 2]])
assert res == 3

res = sol.eraseOverlapIntervals(intervals=[[-5, 0], [0, 5], [5, 10]])
assert res == 0

res = sol.eraseOverlapIntervals(intervals=[[1, 4], [2, 3], [1, 5]])
assert res == 2

res = sol.eraseOverlapIntervals(intervals=[[-50000, 50000]])
assert res == 0
