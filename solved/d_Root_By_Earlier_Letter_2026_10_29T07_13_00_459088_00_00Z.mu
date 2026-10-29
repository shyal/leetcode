# Given n, edges and letters for an undirected tree, return the root.
#
# The tree has n nodes, numbered 0 to n - 1. Each pair [a, b] in edges
# connects nodes a and b. The letter of node i is letters[i].
#
# For an edge connecting nodes of different letters, the end with the
# letter that is lexicographically smaller is the parent. The end with the
# letter that is lexicographically larger is the child. The root is the
# node that is not the child end of any edge.
#
# Example 1:
#
# Input: n = 4, edges = [[0, 1], [0, 2], [1, 3]], letters = "CADF"
# Output: 1
# Explanation: The parent-to-child pairs are 1 to 0, 0 to 2, and 1 to 3.
# Node 1 is not a child end, so it is the root.
#
#     Example 1 rooted at node 1, the letter of each node in parentheses,
#     the parent end above the child end:
#
#               1 (A)
#              /     \
#           0 (C)   3 (F)
#            /
#         2 (D)
#
# Example 2:
#
# Input: n = 2, edges = [[0, 1]], letters = "BA"
# Output: 1
# Explanation: The parent-to-child pair is 1 to 0. Node 1 is not a child
# end, so it is the root.
#
# Example 3:
#
# Input: n = 4, edges = [[0, 1], [1, 2], [2, 3]], letters = "DCBA"
# Output: 3
# Explanation: The parent-to-child pairs are 1 to 0, 2 to 1, and 3 to 2.
# Node 3 is not a child end, so it is the root.
#
# Constraints:
#
#     2 <= n <= 10^5
#     edges.length == n - 1
#     edges is an undirected tree on nodes 0 to n - 1.
#     letters.length == n
#     letters[i] is a capital letter from A to Z.
#     No edge connects two nodes of the same letter.
#     Exactly one node is not a child end.
#
#     REQUIRED: Your solution must run in O(n) time; NO loop that tries
#     each node as the root.
#
# ---

# mu 0.14

class Solution
  def findRoot(n: int, edges: [[int]], values: str) -> int
    child = [false] * n
    for a, b in edges
      child[max(a, b, by=values)] = true
    child.index(false)

sol = Solution()

print(sol.findRoot(4, [[0, 1], [0, 2], [1, 3]], "CADF"))  # 1
draw_graphviz({1: [0, 3], 0: [2]}, directed=true, labels="CADF")  # Example 1, parent above child

assert sol.findRoot(4, [[0, 1], [0, 2], [1, 3]], "CADF") == 1
assert sol.findRoot(4, [[0, 1], [1, 2], [2, 3]], "DCBA") == 3
assert sol.findRoot(2, [[0, 1]], "AB") == 0
assert sol.findRoot(2, [[0, 1]], "BA") == 1
assert sol.findRoot(4, [[2, 0], [2, 1], [3, 2]], "CCBA") == 3  # equal letters on nodes that share no edge
assert sol.findRoot(100000, [[0, i] for i in 1..<100000], "A" + "B" * 99999) == 0
