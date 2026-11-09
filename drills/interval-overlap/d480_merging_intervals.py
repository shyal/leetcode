"""
EPI 13.7 Merging intervals

Given a list disjoint_intervals of closed intervals (left, right),
sorted by left end and pairwise disjoint, and a closed interval
new_interval, return the sorted list of disjoint intervals that covers
exactly the union of all of them. Intervals that overlap, or that share
an end point, become a single interval.

Example 1:

Input: disjoint_intervals = [(1, 2), (4, 6), (8, 10), (13, 15)],
       new_interval = (5, 9)
Output: [(1, 2), (4, 10), (13, 15)]
Explanation: (5, 9) overlaps (4, 6) and (8, 10).

Example 2:

Input: disjoint_intervals = [(1, 3)], new_interval = (5, 7)
Output: [(1, 3), (5, 7)]

Example 3:

Input: disjoint_intervals = [(1, 3), (6, 8)], new_interval = (3, 6)
Output: [(1, 8)]
Explanation: (3, 6) shares the point 3 with (1, 3) and the point 6 with
(6, 8).

Constraints:

    0 <= len(disjoint_intervals) <= 10^5
    -10^9 <= left <= right <= 10^9 for every interval

    REQUIRED: O(n) time, where n is the length of disjoint_intervals.
    NO sorting.
"""


class Solution:
    def add_interval(self, disjoint_intervals: list[tuple[int, int]], new_interval: tuple[int, int]) -> list[tuple[int, int]]:
        pass


sol = Solution()

print(sol.add_interval([(1, 2), (4, 6), (8, 10), (13, 15)], (5, 9)))  # [(1, 2), (4, 10), (13, 15)]

# assert sol.add_interval([(1, 2), (4, 6), (8, 10), (13, 15)], (5, 9)) == [(1, 2), (4, 10), (13, 15)]
# assert sol.add_interval([(1, 3)], (5, 7)) == [(1, 3), (5, 7)]
# assert sol.add_interval([(1, 3), (6, 8)], (3, 6)) == [(1, 8)]
# assert sol.add_interval([], (1, 2)) == [(1, 2)]
# assert sol.add_interval([(5, 7)], (1, 3)) == [(1, 3), (5, 7)]
# assert sol.add_interval([(1, 3), (5, 7)], (0, 10)) == [(0, 10)]
# assert sol.add_interval([(1, 10)], (3, 4)) == [(1, 10)]
# assert sol.add_interval([(1, 3), (8, 9)], (5, 6)) == [(1, 3), (5, 6), (8, 9)]
# assert sol.add_interval([(1, 3), (8, 9)], (4, 7)) == [(1, 3), (4, 7), (8, 9)]
# assert sol.add_interval([(1, 3), (5, 7)], (7, 7)) == [(1, 3), (5, 7)]
# assert sol.add_interval([(1, 3), (5, 7)], (7, 9)) == [(1, 3), (5, 9)]
# assert sol.add_interval([(1, 3), (5, 7)], (-2, 1)) == [(-2, 3), (5, 7)]
# assert sol.add_interval([(2 * i, 2 * i + 1) for i in range(10 ** 5)], (1, 2 * 10 ** 5)) == [(0, 2 * 10 ** 5)]
# assert sol.add_interval([(2 * i, 2 * i) for i in range(10 ** 5)], (10 ** 6, 10 ** 6)) == [(2 * i, 2 * i) for i in range(10 ** 5)] + [(10 ** 6, 10 ** 6)]
# assert sol.add_interval([(2 * i, 2 * i) for i in range(1, 10 ** 5)], (-5, -1)) == [(-5, -1)] + [(2 * i, 2 * i) for i in range(1, 10 ** 5)]
