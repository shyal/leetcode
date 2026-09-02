"""
DRILL: Claim Or Merge
TRAINS: union-find

Given rosters, where rosters[i] is the list of student ids enrolled in
class i, and union, a function where union(a, b) puts classes a and b in
the same group, return the dict owner mapping each student id to the first
class that enrols that student. After your call, two classes that share a
student must be in the same group, and so must two classes joined by a
chain of shared students. Call union on classes only, never on students.
The tests read the groups back through find.

Example 1:

Input: rosters = [[11, 12, 15], [14, 15], [16, 14], [19]]
Output: owner = {11: 0, 12: 0, 15: 0, 14: 1, 16: 2, 19: 3}
        groups = [[0, 1, 2], [3]]
Explanation: student 15 is first listed by class 0 and student 14 by
class 1. Classes 0, 1 and 2 end in one group; class 3 is alone.

Example 2:

Input: rosters = [[13], [13], [13]]
Output: owner = {13: 0}
        groups = [[0, 1, 2]]

Constraints:

    1 <= len(rosters) <= 1000
    1 <= len(rosters[i]) <= 10
    0 <= student id < 10^6
    every class starts in a group of its own

    REQUIRED: must run in O(L) union and dict operations, where L is the
    total roster length. NO class-to-class pair tests; NO second pass over
    rosters.
"""


class Solution:

    def claimOrMerge(self, rosters: List[List[int]], union: Callable[[int, int], bool]) -> Dict[int, int]:
        pass


sol = Solution()


def setup(n):
    parent = [*range(n)]

    def find(x: int) -> int:
        while parent[x] != x:
            x = parent[x]
        return x

    def union(a: int, b: int) -> bool:
        ra = find(a)
        rb = find(b)
        if ra == rb:
            return False
        parent[ra] = rb
        return True

    return parent, find, union


def claim(rosters):
    parent, find, union = setup(len(rosters))
    owner = sol.claimOrMerge(rosters, union)
    groups = {}
    for i in range(len(rosters)):
        groups.setdefault(find(i), []).append(i)
    return owner, sorted(groups.values())


print(claim([[11, 12, 15], [14, 15], [16, 14], [19]]))  # ({11: 0, 12: 0, 15: 0, 14: 1, 16: 2, 19: 3}, [[0, 1, 2], [3]])

# assert claim([[11, 12, 15], [14, 15], [16, 14], [19]]) == ({11: 0, 12: 0, 15: 0, 14: 1, 16: 2, 19: 3}, [[0, 1, 2], [3]])
# assert claim([[13], [13], [13]]) == ({13: 0}, [[0, 1, 2]])
# assert claim([[17]]) == ({17: 0}, [[0]])
# assert claim([[11, 12], [13, 14]]) == ({11: 0, 12: 0, 13: 1, 14: 1}, [[0], [1]])
# assert claim([[11, 12], [13, 14], [12, 13]]) == ({11: 0, 12: 0, 13: 1, 14: 1}, [[0, 1, 2]])
