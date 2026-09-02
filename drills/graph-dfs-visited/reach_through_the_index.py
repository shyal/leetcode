"""
DRILL: Reach Through The Index
TRAINS: graph-dfs-visited

Given rosters, where rosters[i] is the list of student ids enrolled in
class i, and index, a dict mapping each student id to the list of classes
that enrol that student, return the sorted list of classes reachable from
class start. Two classes are connected when they share a student, and a
class is reachable when a chain of zero or more such connections leads to
it from start. The list includes start itself.

Example 1:

Input: rosters = [[11, 12, 15], [14, 15], [16, 14], [19]],
       index = {11: [0], 12: [0], 15: [0, 1], 14: [1, 2], 16: [2], 19: [3]},
       start = 0
Output: [0, 1, 2]
Explanation: student 15 connects class 0 to class 1, and student 14
connects class 1 to class 2. Class 3 shares nobody.

Example 2:

Input: rosters = [[13], [13], [13]], index = {13: [0, 1, 2]}, start = 1
Output: [0, 1, 2]

Constraints:

    1 <= len(rosters) <= 1000
    1 <= len(rosters[i]) <= 10
    0 <= student id < 10^6
    0 <= start < len(rosters)
    index is exactly the inversion of rosters

    REQUIRED: must run in O(L) time, where L is the total roster length.
    NO class-to-class adjacency list built in advance; NO class-to-class
    pair tests.
"""


class Solution:

    def reachableClasses(self, rosters: List[List[int]], index: Dict[int, List[int]], start: int) -> List[int]:
        pass


sol = Solution()


def invert(rosters):
    index = {}
    for i, roster in enumerate(rosters):
        for student in roster:
            index.setdefault(student, []).append(i)
    return index


def reach(rosters, start):
    return sol.reachableClasses(rosters, invert(rosters), start)


print(reach([[11, 12, 15], [14, 15], [16, 14], [19]], 0))  # [0, 1, 2]

# assert reach([[11, 12, 15], [14, 15], [16, 14], [19]], 0) == [0, 1, 2]
# assert reach([[11, 12, 15], [14, 15], [16, 14], [19]], 3) == [3]
# assert reach([[13], [13], [13]], 1) == [0, 1, 2]
# assert reach([[17]], 0) == [0]
# assert reach([[11, 12], [13, 14]], 1) == [1]
# assert reach([[11, 12], [13, 14], [12, 13]], 0) == [0, 1, 2]
