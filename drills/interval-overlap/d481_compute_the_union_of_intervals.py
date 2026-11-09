"""
EPI 13.8 Compute the union of intervals

Given a list of intervals, each a tuple (left, left_closed, right,
right_closed), return the union of the intervals as a list of disjoint
intervals in the same form, sorted by left end. An end is in the
interval when its flag is True and not in it when its flag is False.
Intervals that together cover a range with no gap become a single
interval. Two intervals that meet at a point x join only when at least
one of them contains x.

Example 1:

Input: intervals = [(0, True, 3, False), (3, True, 5, True),
                    (7, False, 9, False), (9, False, 10, True)]
Output: [(0, True, 5, True), (7, False, 9, False), (9, False, 10, True)]
Explanation: [0, 3) and [3, 5] join at 3. The point 9 is in neither
(7, 9) nor (9, 10], so those two stay apart.

Example 2:

Input: intervals = [(1, True, 4, True), (2, False, 3, False)]
Output: [(1, True, 4, True)]

Example 3:

Input: intervals = [(5, False, 6, True), (1, True, 2, True)]
Output: [(1, True, 2, True), (5, False, 6, True)]

Constraints:

    0 <= len(intervals) <= 10^5
    -10^9 <= left <= right <= 10^9
    When left == right, both ends are closed.

    REQUIRED: O(n log n) time, where n is the length of intervals.
"""


class Solution:
    def union_of_intervals(self, intervals: list[tuple[int, bool, int, bool]]) -> list[tuple[int, bool, int, bool]]:
        pass


sol = Solution()

print(sol.union_of_intervals([(0, True, 3, False), (3, True, 5, True), (7, False, 9, False), (9, False, 10, True)]))  # [(0, True, 5, True), (7, False, 9, False), (9, False, 10, True)]

# assert sol.union_of_intervals([(0, True, 3, False), (3, True, 5, True), (7, False, 9, False), (9, False, 10, True)]) == [(0, True, 5, True), (7, False, 9, False), (9, False, 10, True)]
# assert sol.union_of_intervals([(1, True, 4, True), (2, False, 3, False)]) == [(1, True, 4, True)]
# assert sol.union_of_intervals([(5, False, 6, True), (1, True, 2, True)]) == [(1, True, 2, True), (5, False, 6, True)]
# assert sol.union_of_intervals([]) == []
# assert sol.union_of_intervals([(2, False, 4, False)]) == [(2, False, 4, False)]
# assert sol.union_of_intervals([(2, True, 2, True), (2, False, 4, False)]) == [(2, True, 4, False)]
# assert sol.union_of_intervals([(1, False, 2, False), (2, True, 2, True), (2, False, 3, False)]) == [(1, False, 3, False)]
# assert sol.union_of_intervals([(1, False, 5, False), (1, True, 2, True)]) == [(1, True, 5, False)]
# assert sol.union_of_intervals([(0, True, 4, False), (1, True, 4, True)]) == [(0, True, 4, True)]
# assert sol.union_of_intervals([(0, True, 4, True), (1, True, 4, False)]) == [(0, True, 4, True)]
# assert sol.union_of_intervals([(0, False, 10, False), (2, True, 3, True)]) == [(0, False, 10, False)]
# assert sol.union_of_intervals([(0, True, 1, False), (1, False, 2, True)]) == [(0, True, 1, False), (1, False, 2, True)]
# assert sol.union_of_intervals([(0, True, 1, True), (1, False, 2, True)]) == [(0, True, 2, True)]
# assert sol.union_of_intervals([(3, True, 4, True), (0, True, 1, True), (1, True, 3, False)]) == [(0, True, 4, True)]
# assert sol.union_of_intervals([(i, True, i + 1, False) for i in range(10 ** 5)]) == [(0, True, 10 ** 5, False)]
# assert sol.union_of_intervals([(2 * i, False, 2 * i + 1, False) for i in range(10 ** 5, 0, -1)]) == [(2 * i, False, 2 * i + 1, False) for i in range(1, 10 ** 5 + 1)]
