"""
DRILL: Connect To The First Student
TRAINS: graph-adjacency-build

Given rosters, where rosters[i] is the list of student ids enrolled in
class i, return the adjacency dict adj over students. Within each class,
connect every student after the first to the first student of that class,
in both directions, and make no other connection. The list adj[s] holds
the students connected to s, in the order the connections are made, and a
connection made twice appears twice. Every student is a key, so a student
with no connection maps to an empty list.

Example 1:

Input: rosters = [[11, 12, 15], [14, 15], [16, 14], [19]]
Output: {11: [12, 15], 12: [11], 15: [11, 14], 14: [15, 16], 16: [14], 19: []}
Explanation: student 15 is in classes 0 and 1, so 15 is connected to 11
and to 14. Class 3 has one student, so 19 has no connection.

Example 2:

Input: rosters = [[13], [13], [13]]
Output: {13: []}

Constraints:

    1 <= len(rosters) <= 1000
    1 <= len(rosters[i]) <= 10
    0 <= student id < 10^6

    REQUIRED: must run in O(L) time, where L is the total roster length.
    NO class-to-class pair tests; NO all-pairs edges inside a class.
"""

from typing import Dict, List


class Solution:

    def studentGraph(self, rosters: List[List[int]]) -> Dict[int, List[int]]:
        pass


sol = Solution()

print(dict(sol.studentGraph([[11, 12, 15], [14, 15], [16, 14], [19]])))  # {11: [12, 15], 12: [11], 15: [11, 14], 14: [15, 16], 16: [14], 19: []}

# assert sol.studentGraph([[11, 12, 15], [14, 15], [16, 14], [19]]) == {11: [12, 15], 12: [11], 15: [11, 14], 14: [15, 16], 16: [14], 19: []}
# assert sol.studentGraph([[13], [13], [13]]) == {13: []}
# assert sol.studentGraph([[17]]) == {17: []}
# assert sol.studentGraph([[11, 12], [13, 14]]) == {11: [12], 12: [11], 13: [14], 14: [13]}
# assert sol.studentGraph([[11, 12], [12, 11]]) == {11: [12, 12], 12: [11, 11]}
