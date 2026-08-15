"""
DRILL: Build Parents and Find Roots
TRAINS: union-find

n nodes form a forest of rooted trees. Every node has exactly one edge
pointing up at its parent; a root points at itself. The whole forest is
stored as a single list: parent[i] is the node that i points at.

Implement buildFind(n):
  - build the starting forest, where every node is its own root
  - define find(x): follow the edges up from x and return the root of
    its tree
  - return the pair (parent, find)

The caller repoints edges over time (parent[1] = 0 hangs node 1 under
node 0); find must always walk the edges as they are now.

Example:

    parent, find = sol.buildFind(4)
    parent starts as [0, 1, 2, 3] -> four one-node trees
    find(2) -> 2

    parent[1] = 0
    parent[2] = 1
    parent is now [0, 0, 1, 3] -> a chain under 0, and 3 alone
    find(2): 2 -> 1 -> 0    root 0

  0        3
  |
  1
  |
  2

Constraints:

    1 <= n <= 1000
    parent always describes a forest when find is called

    REQUIRED: parent = [...] init + the find hop loop (or recursion).
    Path compression optional.
"""


class Solution:
    def buildFind(self, n: int):
        pass


sol = Solution()

parent, find = sol.buildFind(4)
assert parent == [0, 1, 2, 3]
assert [find(x) for x in range(4)] == [0, 1, 2, 3]

parent[1] = 0
parent[2] = 1
assert find(2) == 0
assert find(1) == 0
assert find(3) == 3

parent, find = sol.buildFind(5)
parent[0] = 1
parent[1] = 2
parent[2] = 3
parent[3] = 4
assert find(0) == 4
assert find(4) == 4

parent, find = sol.buildFind(1)
assert find(0) == 0

print("All tests passed!")
