"""
Given two lists of free time slots, slotsA and slotsB, and a duration
dur, return the earliest slot [start, start + dur] that lies inside a
slot of slotsA and inside a slot of slotsB. Return [] when there is
none. A slot is [start, end] in seconds, and a slot [s, e] lies inside
[a, b] when a <= s and e <= b. In each list the slots are disjoint and
sorted by start.

Example 1:

Input: slotsA = [[10, 50], [60, 120], [140, 210]]
       slotsB = [[0, 15], [60, 70]]
       dur = 8
Output: [60, 68]
Explanation: [10, 50] and [0, 15] share only [10, 15], five seconds.
[60, 120] and [60, 70] share [60, 70], ten seconds.

Example 2:

Input: slotsA = [[10, 50], [60, 120], [140, 210]]
       slotsB = [[0, 15], [60, 70]]
       dur = 12
Output: []

Example 3:

Input: slotsA = [[1, 10]], slotsB = [[2, 3], [5, 7]], dur = 2
Output: [5, 7]
Explanation: [2, 3] is one second.

Constraints:

    1 <= len(slotsA), len(slotsB) <= 10^5
    slotsA[i] = [start, end] with 0 <= start < end <= 2^31 - 1
    1 <= dur <= 2^31 - 1

    REQUIRED: O(len(slotsA) + len(slotsB)) time, O(1) extra space. NO
    comparison of every slot of slotsA with every slot of slotsB.
"""


class Solution:
    def meeting_planner(self, slotsA: list[list[int]], slotsB: list[list[int]], dur: int) -> list[int]:
        pass


sol = Solution()

print(sol.meeting_planner([[10, 50], [60, 120], [140, 210]], [[0, 15], [60, 70]], 8))  # [60, 68]

# assert sol.meeting_planner([[10, 50], [60, 120], [140, 210]], [[0, 15], [60, 70]], 8) == [60, 68]
# assert sol.meeting_planner([[10, 50], [60, 120], [140, 210]], [[0, 15], [60, 70]], 12) == []
# assert sol.meeting_planner([[1, 10]], [[2, 3], [5, 7]], 2) == [5, 7]
# assert sol.meeting_planner([[7, 12]], [[2, 11]], 5) == []
# assert sol.meeting_planner([[6, 12]], [[2, 11]], 5) == [6, 11]
# assert sol.meeting_planner([[0, 5], [50, 70], [120, 125]], [[0, 50]], 8) == []
# assert sol.meeting_planner([[10, 50], [60, 120], [140, 210]], [[0, 15], [60, 72]], 12) == [60, 72]
# assert sol.meeting_planner([[0, 10]], [[0, 10]], 10) == [0, 10]
# assert sol.meeting_planner([[0, 10]], [[0, 10]], 11) == []
# assert sol.meeting_planner([[0, 10]], [[10, 20]], 1) == []
# assert sol.meeting_planner([[0, 100]], [[10, 20], [30, 40]], 5) == [10, 15]
# assert sol.meeting_planner([[10, 20], [30, 40]], [[0, 100]], 5) == [10, 15]
# assert sol.meeting_planner([[0, 1]], [[0, 1]], 1) == [0, 1]
# assert sol.meeting_planner([[0, 2 ** 31 - 1]], [[0, 2 ** 31 - 1]], 2 ** 31 - 1) == [0, 2 ** 31 - 1]
# assert sol.meeting_planner([[2 * i, 2 * i + 1] for i in range(10 ** 5)], [[2 * i + 1, 2 * i + 2] for i in range(10 ** 5)], 1) == []
# assert sol.meeting_planner([[3 * i, 3 * i + 2] for i in range(10 ** 5)], [[3 * i + 1, 3 * i + 3] for i in range(10 ** 5)], 1) == [1, 2]
# assert sol.meeting_planner([[3 * i, 3 * i + 2] for i in range(10 ** 5)], [[3 * i + 1, 3 * i + 3] for i in range(10 ** 5)], 2) == []
