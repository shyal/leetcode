"""
EPI 17.3 The interval covering problem

Given a list intervals of closed intervals [left, right], return the
smallest number of points such that each interval holds at least one of
the points. A point x is in [left, right] when left <= x <= right.

Example 1:

Input: intervals = [[0, 3], [2, 6], [3, 4], [6, 9]]
Output: 2
Explanation: the points 3 and 6 work. No single point is in both [0, 3]
and [6, 9].

Example 2:

Input: intervals = [[1, 1], [2, 2]]
Output: 2

Example 3:

Input: intervals = []
Output: 0

Constraints:

    0 <= len(intervals) <= 10^5
    0 <= left <= right <= 10^9

    REQUIRED: O(n log n) time for n intervals.
"""


class Solution:
    def find_minimum_visits(self, intervals: list[list[int]]) -> int:
        pass


sol = Solution()

print(sol.find_minimum_visits([[0, 3], [2, 6], [3, 4], [6, 9]]))  # 2

# assert sol.find_minimum_visits([[0, 3], [2, 6], [3, 4], [6, 9]]) == 2
# assert sol.find_minimum_visits([[1, 1], [2, 2]]) == 2
# assert sol.find_minimum_visits([]) == 0
# assert sol.find_minimum_visits([[4, 4]]) == 1
# assert sol.find_minimum_visits([[0, 10], [1, 2], [3, 4], [5, 6]]) == 3
# assert sol.find_minimum_visits([[1, 5], [2, 6], [3, 7]]) == 1
# assert sol.find_minimum_visits([[1, 3], [5, 8], [2, 6], [7, 9], [0, 1]]) == 3
# assert sol.find_minimum_visits([[1, 2], [1, 2]]) == 1
# assert sol.find_minimum_visits([[1, 2], [2, 3]]) == 1
# assert sol.find_minimum_visits([[0, 100], [50, 50]]) == 1
# assert sol.find_minimum_visits([[6, 9], [3, 4], [2, 6], [0, 3]]) == 2
# assert sol.find_minimum_visits([[0, 1000000000], [1000000000, 1000000000]]) == 1
# assert sol.find_minimum_visits([[i, i] for i in range(100000)]) == 100000
# assert sol.find_minimum_visits([[0, 10**9]] * 100000) == 1
# assert sol.find_minimum_visits([[i, i + 1] for i in range(100000)]) == 50000
# assert sol.find_minimum_visits([[i, 10**9 - i] for i in range(100000)]) == 1
