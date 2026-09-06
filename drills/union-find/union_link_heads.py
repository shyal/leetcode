"""
DRILL: Union Links Head to Head
TRAINS: union-find
SNIPPET: lcunionunion

Given employees a and b, merge their companies and return True, or return
False when they are already one company. Solution extends UnionFind from
dsa/union_find.py: self.parent[i] is the manager of employee i, an
employee who is their own manager is a head, and self.find(x) returns the
head of x. Write union so that the head of a reports to the head of b.
Neither a nor b moves. Management chains never contain cycles.

Example 1:

Input: parent = [1, 2, 2, 4, 5, 5], union(0, 3)
Output: True, parent = [1, 2, 5, 4, 5, 5]
Explanation: the head of 0 is 2 and the head of 3 is 5. Only the entry of
2 changes.

Example 2:

Input: parent = [1, 2, 2, 3], union(0, 1)
Output: False, parent unchanged
Explanation: 0 and 1 both have head 2.

Constraints:

    1 <= n <= 1000
    0 <= a, b < n
    parent is free of cycles whenever union is called

    REQUIRED: must change at most one entry of self.parent per call. NO
    reassignment of a or b themselves; NO find of your own.
"""

from dsa.union_find import UnionFind


class Solution(UnionFind):
    def union(self, a: int, b: int) -> bool:
        pass


sol = Solution(6)
sol.parent[0] = 1
sol.parent[1] = 2
sol.parent[3] = 4
sol.parent[4] = 5
sol.union(0, 3)

print(sol.parent)  # [1, 2, 5, 4, 5, 5]

## two people
# sol = Solution(2)
# assert sol.union(0, 1) is True
# assert sol.parent == [1, 1]

## fresh singletons, hang 0 under 1, leave 2 and 3 alone
# sol = Solution(4)
# sol.union(0, 1)
# assert sol.parent == [1, 1, 2, 3]

## hang 2 under 0
# sol = Solution(4)
# sol.union(2, 0)
# assert sol.parent == [0, 1, 0, 3]

## example 1 - two chains, union the leaves
# sol = Solution(6)
# sol.parent[0] = 1
# sol.parent[1] = 2
# sol.parent[3] = 4
# sol.parent[4] = 5
# assert sol.union(0, 3) is True
# assert sol.parent == [1, 2, 5, 4, 5, 5]

## example 2 - already the same company
# sol = Solution(4)
# sol.parent[0] = 1
# sol.parent[1] = 2
# assert sol.union(0, 1) is False
# assert sol.parent == [1, 2, 2, 3]

## union with self is a no-op
# sol = Solution(3)
# assert sol.union(0, 0) is False
# assert sol.parent == [0, 1, 2]

## two mergers, then merge the companies via leaves
# sol = Solution(4)
# sol.union(0, 1)
# assert sol.parent == [1, 1, 2, 3]
# sol.union(2, 3)
# assert sol.parent == [1, 1, 3, 3]
# sol.union(0, 2)
# assert sol.parent == [1, 3, 3, 3]

## n = 1
# sol = Solution(1)
# sol.union(0, 0)
# assert sol.parent == [0]
