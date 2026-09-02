"""
DRILL: Rosters By Head
TRAINS: union-find

Given rosters, where rosters[i] is the list of student ids enrolled in
class i, and find, a function where find(i) returns the head of the group
that class i belongs to, return one merged roster per group. A merged
roster is the sorted list of distinct student ids across the classes of
its group. Order the merged rosters by the smallest class index in each
group.

Example 1:

Input: rosters = [[11, 12, 15], [14, 15], [16, 14], [19]],
       groups = [[0, 1, 2], [3]]
Output: [[11, 12, 14, 15, 16], [19]]
Explanation: classes 0, 1 and 2 share a head, so their students form one
roster, with 14 and 15 listed once each. Class 3 is a group of its own.

Example 2:

Input: rosters = [[13], [13], [13]], groups = [[0, 1, 2]]
Output: [[13]]

Constraints:

    1 <= len(rosters) <= 1000
    1 <= len(rosters[i]) <= 10
    0 <= student id < 10^6
    the tests build find from groups before calling you

    REQUIRED: must call find at most once per class. NO class-to-class
    pair tests; NO scan for heads other than through find.
"""


class Solution:

    def mergeRosters(self, rosters: List[List[int]], find: Callable[[int], int]) -> List[List[int]]:
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


def merged(rosters, groups):
    parent, find, union = setup(len(rosters))
    for group in groups:
        for a, b in zip(group, group[1:]):
            union(a, b)
    return sol.mergeRosters(rosters, find)


print(merged([[11, 12, 15], [14, 15], [16, 14], [19]], [[0, 1, 2], [3]]))  # [[11, 12, 14, 15, 16], [19]]

# assert merged([[11, 12, 15], [14, 15], [16, 14], [19]], [[0, 1, 2], [3]]) == [[11, 12, 14, 15, 16], [19]]
# assert merged([[13], [13], [13]], [[0, 1, 2]]) == [[13]]
# assert merged([[17]], [[0]]) == [[17]]
# assert merged([[11, 12], [13, 14]], [[0], [1]]) == [[11, 12], [13, 14]]
# assert merged([[19], [11, 12], [13, 14], [12, 13]], [[0], [1, 2, 3]]) == [[19], [11, 12, 13, 14]]
