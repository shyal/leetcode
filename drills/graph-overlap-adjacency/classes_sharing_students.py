"""
DRILL: Classes Sharing A Student
TRAINS: graph-overlap-adjacency

Given rosters, where rosters[i] is the list of student ids enrolled in
class i, two classes are connected when at least one student is enrolled
in both. Return the adjacency list adj, where adj[i] is the list of
indexes of the classes connected to class i, in increasing order. A class
is never connected to itself.

Example 1:

Input: rosters = [[11, 12, 15], [14, 15], [16, 14], [19]]
Output: [[1], [0, 2], [1], []]
Explanation: student 15 is in classes 0 and 1, student 14 is in classes
1 and 2, and class 3 shares nobody.

Example 2:

Input: rosters = [[13], [13], [13]]
Output: [[1, 2], [0, 2], [0, 1]]

Constraints:

    1 <= len(rosters) <= 500
    1 <= len(rosters[i]) <= 10^5
    sum(len(rosters[i])) <= 10^5
    0 <= student id < 10^6

    REQUIRED: must run in O(n * L) time, where n is the number of classes
    and L is the total roster length. NO student-to-student edges; NO
    element-by-element pair tests.
"""

from typing import List


class Solution:

    def classGraph(self, rosters: List[List[int]]) -> List[List[int]]:
        pass


sol = Solution()

print(sol.classGraph([[11, 12, 15], [14, 15], [16, 14], [19]]))  # [[1], [0, 2], [1], []]

# assert sol.classGraph([[11, 12, 15], [14, 15], [16, 14], [19]]) == [[1], [0, 2], [1], []]
# assert sol.classGraph([[13], [13], [13]]) == [[1, 2], [0, 2], [0, 1]]
# assert sol.classGraph([[17]]) == [[]]
# assert sol.classGraph([[11, 12], [13, 14]]) == [[], []]
