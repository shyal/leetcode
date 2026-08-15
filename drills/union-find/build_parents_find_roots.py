"""
DRILL: Build Parents and Find Roots
TRAINS: union-find

Write buildFind(n): create the parent list for n nodes and define find(x)
inside it. Return the pair (parent, find).

The tests rewire parent directly (parent[1] = 0 and so on) and then call
your find — so all you write is the data structure and the hop. No union,
no edges, no wrapper problem.

Example:

    parent, find = sol.buildFind(4)
    parent starts as [0, 1, 2, 3] -> every node is its own root
    find(2) -> 2

    parent[1] = 0
    parent[2] = 1
    parent is now [0, 0, 1, 3]
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
