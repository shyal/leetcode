"""
EPI 13.6 Render a calendar

Given a list A of events, each a pair (start, finish) of integer times
with start <= finish, return the largest number of events that take
place at the same time. An event takes place at every time from start to
finish, both ends included, so two events that share an end time take
place at the same time.

Example 1:

Input: A = [(1, 4), (2, 6), (3, 5), (7, 8)]
Output: 3
Explanation: at time 3 the first three events take place.

Example 2:

Input: A = [(1, 2), (2, 3)]
Output: 2
Explanation: both events take place at time 2.

Example 3:

Input: A = []
Output: 0

Constraints:

    0 <= len(A) <= 10^5
    0 <= start <= finish <= 10^9

    REQUIRED: O(n log n) time, where n is the length of A. NO check of
    every pair of events. NO loop over every time unit.
"""


class Solution:
    def find_max_simultaneous_events(self, A: list[tuple[int, int]]) -> int:
        pass


sol = Solution()

print(sol.find_max_simultaneous_events([(1, 4), (2, 6), (3, 5), (7, 8)]))  # 3

# assert sol.find_max_simultaneous_events([(1, 4), (2, 6), (3, 5), (7, 8)]) == 3
# assert sol.find_max_simultaneous_events([(1, 2), (2, 3)]) == 2
# assert sol.find_max_simultaneous_events([]) == 0
# assert sol.find_max_simultaneous_events([(5, 5)]) == 1
# assert sol.find_max_simultaneous_events([(5, 5), (5, 5)]) == 2
# assert sol.find_max_simultaneous_events([(1, 2), (3, 4)]) == 1
# assert sol.find_max_simultaneous_events([(1, 10), (2, 3), (4, 5), (6, 7)]) == 2
# assert sol.find_max_simultaneous_events([(1, 3)] * 5) == 5
# assert sol.find_max_simultaneous_events([(0, 1), (1, 2), (2, 3), (3, 4)]) == 2
# assert sol.find_max_simultaneous_events([(6, 9), (1, 2), (8, 8), (0, 6)]) == 2
# assert sol.find_max_simultaneous_events([(0, 10 ** 9), (10 ** 9, 10 ** 9), (0, 0)]) == 2
# assert sol.find_max_simultaneous_events([(i, i + 1) for i in range(0, 2 * 10 ** 5, 2)]) == 1
# assert sol.find_max_simultaneous_events([(i, 10 ** 6) for i in range(10 ** 5)]) == 10 ** 5
# assert sol.find_max_simultaneous_events([(i, i + 2) for i in range(10 ** 5)]) == 3
