"""
Given a list data of door readings, return the timestamp at which the
mall held the most people. A reading is [timestamp, count, direction]:
count people passed the door at that timestamp, direction 1 means they
entered and 0 means they left. The number of people in the mall before
the first reading is 0. The readings are sorted by timestamp, and
several readings can share one timestamp. The number of people at a
timestamp is the number after every reading with that timestamp. When
several timestamps tie for the most people, return the earliest.

Example 1:

Input: data = [[1487799425, 14, 1], [1487799425, 4, 0],
               [1487799425, 2, 0], [1487800378, 10, 1],
               [1487801478, 18, 0], [1487801478, 19, 1],
               [1487801478, 1, 0], [1487801478, 1, 1],
               [1487901013, 1, 0], [1487901211, 7, 1],
               [1487901211, 8, 0]]
Output: 1487801478
Explanation: the number of people after each timestamp is 8, 18, 19,
18, 17. Reading the 19 entrances at 1487801478 on their own gives 37,
but the 18 and 1 exits at the same timestamp count too.

Example 2:

Input: data = [[1487799425, 21, 1], [1487799425, 4, 0], [1487901318, 7, 0]]
Output: 1487799425
Explanation: 17 people after the first timestamp, 10 after the second.

Example 3:

Input: data = [[1487799425, 14, 1], [1487800378, 10, 1],
               [1487801478, 24, 0], [1487901211, 24, 1]]
Output: 1487800378
Explanation: 14, 24, 0, 24. Two timestamps hold 24; the earliest of
them is the second reading. The answer is 1487800378.

Constraints:

    1 <= len(data) <= 10^5
    data[i] = [timestamp, count, direction]
    0 <= timestamp <= 2^31 - 1
    1 <= count <= 10^4
    direction is 0 or 1
    data is sorted by timestamp.

    REQUIRED: O(n) time, O(1) extra space, one pass. NO sorting, NO
    dict or list of per-timestamp totals.
"""


class Solution:
    def find_busiest_period(self, data: list[list[int]]) -> int:
        pass


sol = Solution()

print(sol.find_busiest_period([[1487799425, 14, 1], [1487799425, 4, 0], [1487799425, 2, 0], [1487800378, 10, 1], [1487801478, 18, 0], [1487801478, 19, 1], [1487801478, 1, 0], [1487801478, 1, 1], [1487901013, 1, 0], [1487901211, 7, 1], [1487901211, 8, 0]]))  # 1487801478

# assert sol.find_busiest_period([[1487799425, 14, 1], [1487799425, 4, 0], [1487799425, 2, 0], [1487800378, 10, 1], [1487801478, 18, 0], [1487801478, 19, 1], [1487801478, 1, 0], [1487801478, 1, 1], [1487901013, 1, 0], [1487901211, 7, 1], [1487901211, 8, 0]]) == 1487801478
# assert sol.find_busiest_period([[1487799425, 21, 1], [1487799425, 4, 0], [1487901318, 7, 0]]) == 1487799425
# assert sol.find_busiest_period([[1487799425, 14, 1], [1487800378, 10, 1], [1487801478, 24, 0], [1487901211, 24, 1]]) == 1487800378
# assert sol.find_busiest_period([[1487799426, 21, 1]]) == 1487799426
# assert sol.find_busiest_period([[1487799425, 21, 0], [1487799427, 22, 1], [1487901318, 7, 0]]) == 1487799427
# assert sol.find_busiest_period([[1487799425, 14, 1], [1487799425, 4, 0], [1487799425, 2, 0], [1487800378, 10, 1], [1487801478, 18, 0], [1487801478, 18, 1], [1487901013, 1, 0], [1487901211, 7, 1], [1487901211, 7, 0]]) == 1487800378
# assert sol.find_busiest_period([[1487799425, 14, 1], [1487799425, 4, 1], [1487799425, 2, 1], [1487800378, 10, 1], [1487801478, 18, 1], [1487901013, 1, 1], [1487901211, 7, 1], [1487901211, 7, 1]]) == 1487901211
# assert sol.find_busiest_period([[5, 3, 1], [5, 3, 0], [6, 1, 1]]) == 6
# assert sol.find_busiest_period([[5, 3, 1], [5, 3, 0], [6, 3, 1], [6, 3, 0]]) == 5
# assert sol.find_busiest_period([[0, 1, 1], [2 ** 31 - 1, 1, 1]]) == 2 ** 31 - 1
# assert sol.find_busiest_period([[t, 1, 1] for t in range(10 ** 5)]) == 10 ** 5 - 1
# assert sol.find_busiest_period([[t, 1, 1] for t in range(10 ** 5)] + [[10 ** 5, 10 ** 4, 0]]) == 10 ** 5 - 1
# assert sol.find_busiest_period([[0, 10 ** 4, 1]] + [[t, 1, 0] for t in range(1, 10 ** 5)]) == 0
