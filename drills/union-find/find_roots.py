"""
DRILL: Find Roots in a Parent Array
TRAINS: union-find

You are given a hand-built parent array. parent[i] is the parent of node i;
a node whose parent is itself is a root. Following parents always reaches
a root.

For each node in queries, return the root of the group it belongs to.

No union here — this drill is find only.

Example 1:

Input: parent = [0, 0, 1, 3], queries = [2, 3, 1]
Output: [0, 3, 0]
Explanation:
    find(2): 2 -> 1 -> 0    root 0
    find(3): 3 is its own parent, root 3
    find(1): 1 -> 0         root 0

  0        3
  |
  1
  |
  2

Example 2:

Input: parent = [1, 2, 3, 4, 4], queries = [0, 2, 4]
Output: [4, 4, 4]
Explanation: one long chain hanging under 4.

  4
  |
  3
  |
  2
  |
  1
  |
  0

Constraints:

    1 <= len(parent) <= 1000
    parent describes a forest: following parents always terminates at a root
    0 <= q < len(parent) for every q in queries

    REQUIRED: the find hop loop (or recursion). Path compression optional.
"""


class Solution:
    def findRoots(self, parent: list[int], queries: list[int]) -> list[int]:
        pass


sol = Solution()

assert sol.findRoots([0, 0, 1, 3], [2, 3, 1]) == [0, 3, 0]
assert sol.findRoots([1, 2, 3, 4, 4], [0, 2, 4]) == [4, 4, 4]
assert sol.findRoots([0, 1, 2], [0, 1, 2]) == [0, 1, 2]
assert sol.findRoots([0], [0, 0]) == [0, 0]
assert sol.findRoots([0, 0, 0, 3, 3, 4], [1, 2, 5, 4]) == [0, 0, 3, 3]
assert sol.findRoots([0, 0, 1, 3], []) == []

print("All tests passed!")
