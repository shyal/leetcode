"""
DRILL: Even Length Walks

Given an integer n and a list edges of directed edges [a, b] on nodes 0 to
n - 1, return an array ans of length n. Entry ans[x] is the length of the
shortest walk from node 0 to node x that uses an even number of edges, or
-1 if no such walk exists. A walk may repeat nodes and edges. The empty
walk from 0 to 0 has length 0.

Example 1:

Input: n = 4, edges = [[0, 1], [1, 2], [2, 3], [3, 1]]
Output: [0, 4, 2, 6]
Explanation: 0 -> 1 has length 1, which is odd. The walk 0 -> 1 -> 2 -> 3
-> 1 has length 4. Node 3 is reached at length 3, then again at length 6
after one more turn of the cycle 1 -> 2 -> 3 -> 1.

Example 2:

Input: n = 3, edges = [[0, 1], [1, 2]]
Output: [0, -1, 2]

Example 3:

Input: n = 3, edges = [[0, 1], [1, 1]]
Output: [0, 2, -1]
Explanation: The self edge 1 -> 1 makes 0 -> 1 -> 1 a walk of length 2.

Constraints:

    1 <= n <= 100
    0 <= len(edges) <= 400
    0 <= a, b < n

    REQUIRED: O(n + m), one breadth-first search from node 0. NO search
    per target node. A visited set keyed on the node alone returns -1 for
    node 1 in Example 1.
"""


class Solution:

    def evenWalks(self, n: int, edges: List[List[int]]) -> List[int]:
        pass


sol = Solution()

draw_graphviz([[0, 1], [1, 2], [2, 3], [3, 1]], n=4, type="directed")
print(sol.evenWalks(4, [[0, 1], [1, 2], [2, 3], [3, 1]]))  # [0, 4, 2, 6]

# assert sol.evenWalks(4, [[0, 1], [1, 2], [2, 3], [3, 1]]) == [0, 4, 2, 6]
# assert sol.evenWalks(4, [[0, 1], [1, 2], [2, 1], [2, 3]]) == [0, -1, 2, -1]
# assert sol.evenWalks(3, [[0, 1], [1, 2]]) == [0, -1, 2]
# assert sol.evenWalks(3, [[0, 1], [1, 1]]) == [0, 2, -1]
# assert sol.evenWalks(1, []) == [0]
# assert sol.evenWalks(2, [[0, 1], [1, 0]]) == [0, -1]
# assert sol.evenWalks(3, [[0, 1], [0, 2], [1, 2], [2, 0]]) == [0, 4, 2]
# assert sol.evenWalks(4, [[0, 1], [0, 2], [1, 3], [2, 3]]) == [0, -1, -1, 2]
# assert sol.evenWalks(5, [[0, 1], [1, 2], [2, 3], [3, 4], [4, 4]]) == [0, -1, 2, -1, 4]
# assert sol.evenWalks(10, [[i, i + 1] for i in range(9)]) == [0, -1, 2, -1, 4, -1, 6, -1, 8, -1]
# assert sol.evenWalks(6, [[0, 1], [1, 2], [2, 0], [2, 3], [3, 4], [4, 5]]) == [0, 4, 2, 6, 4, 8]
# assert sol.evenWalks(3, [[1, 2], [2, 1]]) == [0, -1, -1]
