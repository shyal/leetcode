"""
Given edges of an undirected tree and node values, return the root or -1
if no root exists.

The tree has nodes 0 through n - 1. Each pair [a, b] in edges connects
nodes a and b. The value of node i is values[i].

If both ends of an edge have equal values, return -1. For each edge, the
end with the smaller value is the parent end. The end with the larger
value is the child end. The root is the node that is not the child end
of any edge. If a node is the child end of two edges, return -1.
Otherwise, return the root.

Example 1:

Input: edges = [[0, 1], [0, 2], [1, 3]], values = [5, 2, 7, 9]
Output: 1
Explanation: For [0, 1], node 1 is the parent end and node 0 is the
child end. For [0, 2], node 2 is the child end. For [1, 3], node 3 is
the child end. Node 1 is not a child end.

Example 2:

Input: edges = [[0, 1]], values = [4, 4]
Output: -1
Explanation: Both ends of [0, 1] have value 4.

Example 3:

Input: edges = [[0, 1], [1, 2]], values = [1, 5, 2]
Output: -1
Explanation: Node 1 is the child end of both edges. Nodes 0 and 2 are
not child ends.

Constraints:

    2 <= n <= 10^5
    edges.length == n - 1
    Each edge is a pair [a, b] with 0 <= a, b < n.
    edges is an undirected tree.
    values.length == n
    0 <= values[i] <= 10^9

    REQUIRED: Your solution must run in O(n) time, with NO loop that
    tries each node as the root.
"""


class Solution:
    def findRoot(self, edges: list[list[int]], values: list[int]) -> int:
        pass


sol = Solution()

print(sol.findRoot([[0, 1], [0, 2], [1, 3]], [5, 2, 7, 9]))  # 1

# assert sol.findRoot([[0, 1], [0, 2], [1, 3]], [5, 2, 7, 9]) == 1
# assert sol.findRoot([[0, 1]], [4, 4]) == -1
# assert sol.findRoot([[0, 1], [1, 2]], [1, 5, 2]) == -1
# assert sol.findRoot([[0, 1]], [3, 8]) == 0
# assert sol.findRoot([[0, 1]], [8, 3]) == 1
# assert sol.findRoot([[0, 1], [1, 2], [2, 3]], [9, 7, 5, 3]) == 3  # chain, root at the far end
# assert sol.findRoot([[2, 0], [2, 1], [3, 2]], [6, 6, 4, 1]) == 3  # equal values on nodes that share no edge
# assert sol.findRoot([[i, i + 1] for i in range(99999)], list(range(100000, 0, -1))) == 99999
