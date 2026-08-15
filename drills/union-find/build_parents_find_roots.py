"""
DRILL: Build Parents and Find Roots
TRAINS: union-find

Given n nodes labeled 0..n-1 and a list of links [c, p] meaning "node c's
parent becomes node p", apply the links in order. The links are guaranteed
to form a forest (no cycles, each c is linked at most once).

Then, for each node in queries, return the root of its group.

This drill is the parent array + find, no union: you build the array,
apply the links literally, and hop to roots.

Example 1:

Input: n = 4, links = [[1,0],[2,1]], queries = [2, 3]
Output: [0, 3]
Explanation:
    start          parent = [0, 1, 2, 3]
    link [1,0] ->  parent = [0, 0, 2, 3]
    link [2,1] ->  parent = [0, 0, 1, 3]
    find(2): 2 -> 1 -> 0    root 0
    find(3): 3 is its own parent, root 3

  0        3
  |
  1
  |
  2

Example 2:

Input: n = 5, links = [[0,1],[1,2],[2,3],[3,4]], queries = [0, 2]
Output: [4, 4]
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

    1 <= n <= 1000
    links form a forest; 0 <= c, p < n
    0 <= q < n for every q in queries

    REQUIRED: parent = [...] init, apply links, then the find hop loop
    (or recursion). Path compression optional.
"""


class Solution:
    def buildAndFind(self, n: int, links: list[list[int]], queries: list[int]) -> list[int]:
        pass


sol = Solution()

assert sol.buildAndFind(4, [[1, 0], [2, 1]], [2, 3]) == [0, 3]
assert sol.buildAndFind(5, [[0, 1], [1, 2], [2, 3], [3, 4]], [0, 2]) == [4, 4]
assert sol.buildAndFind(3, [], [0, 1, 2]) == [0, 1, 2]
assert sol.buildAndFind(6, [[1, 0], [2, 0], [4, 3], [5, 4]], [2, 5, 3, 1]) == [0, 3, 3, 0]
assert sol.buildAndFind(1, [], [0]) == [0]
assert sol.buildAndFind(4, [[1, 0], [2, 1]], []) == []

print("All tests passed!")
