"""
DRILL: Exact Length Walks

Given an integer n, a list edges of directed edges [a, b] on nodes 0 to
n - 1, and an integer k, return the nodes that a walk of exactly k edges
from node 0 reaches, in any order. A walk may repeat nodes and edges. The
empty walk reaches node 0 with 0 edges.

Example 1:

Input: n = 4, edges = [[0, 1], [1, 2], [2, 3], [3, 1]], k = 4
Output: [1]
Explanation: The walk 0 -> 1 -> 2 -> 3 -> 1 has 4 edges. Node 1 is also
reached with 1 edge, but no other node is reached with exactly 4.

Example 2:

Input: n = 3, edges = [[0, 1], [0, 2], [1, 2], [2, 0]], k = 2
Output: [0, 2]
Explanation: 0 -> 1 -> 2 and 0 -> 2 -> 0.

Example 3:

Input: n = 3, edges = [[0, 1], [1, 2]], k = 3
Output: []

Constraints:

    1 <= n <= 100
    0 <= len(edges) <= 400
    0 <= a, b < n
    0 <= k <= 100

    REQUIRED: O(k * (n + m)), one breadth-first search from node 0. NO
    search per target node. A visited set keyed on the node alone returns
    [] for Example 1.
"""


class Solution:

    def exactWalks(self, n: int, edges: List[List[int]], k: int) -> List[int]:
        pass


sol = Solution()

draw_graphviz([[0, 1], [1, 2], [2, 3], [3, 1]], n=4, type="directed")
print(sol.exactWalks(4, [[0, 1], [1, 2], [2, 3], [3, 1]], 4))  # [1]

# assert sorted(sol.exactWalks(4, [[0, 1], [1, 2], [2, 3], [3, 1]], 4)) == [1]
# assert sorted(sol.exactWalks(4, [[0, 1], [1, 2], [2, 3], [3, 1]], 0)) == [0]
# assert sorted(sol.exactWalks(4, [[0, 1], [1, 2], [2, 3], [3, 1]], 3)) == [3]
# assert sorted(sol.exactWalks(4, [[0, 1], [1, 2], [2, 3], [3, 1]], 7)) == [1]
# assert sorted(sol.exactWalks(3, [[0, 1], [1, 2]], 2)) == [2]
# assert sorted(sol.exactWalks(3, [[0, 1], [1, 2]], 3)) == []
# assert sorted(sol.exactWalks(3, [[0, 1], [1, 1]], 5)) == [1]
# assert sorted(sol.exactWalks(1, [], 0)) == [0]
# assert sorted(sol.exactWalks(1, [], 1)) == []
# assert sorted(sol.exactWalks(2, [[0, 1], [1, 0]], 6)) == [0]
# assert sorted(sol.exactWalks(2, [[0, 1], [1, 0]], 7)) == [1]
# assert sorted(sol.exactWalks(3, [[0, 1], [0, 2], [1, 2], [2, 0]], 2)) == [0, 2]
# assert sorted(sol.exactWalks(4, [[0, 1], [0, 2], [1, 3], [2, 3]], 1)) == [1, 2]
# assert sorted(sol.exactWalks(4, [[0, 1], [0, 2], [1, 3], [2, 3]], 2)) == [3]
# assert sorted(sol.exactWalks(10, [[i, i + 1] for i in range(9)], 9)) == [9]
# assert sorted(sol.exactWalks(6, [[0, 1], [1, 2], [2, 0], [2, 3], [3, 4], [4, 5]], 5)) == [2, 5]
# assert sorted(sol.exactWalks(6, [[0, 1], [1, 2], [2, 0], [2, 3], [3, 4], [4, 5]], 8)) == [2, 5]
# assert sorted(sol.exactWalks(3, [[1, 2], [2, 1]], 2)) == []
