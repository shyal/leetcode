"""
DRILL: Count In-Degrees

Given n nodes numbered 0 to n - 1 and edges, where [a, b] is an edge
from a to b, return indeg, where indeg[b] is the number of edges into b.

Example 1:

Input: n = 4, edges = [[0, 1], [0, 2], [1, 3], [2, 3]]

    0 --> 1 --.
    |         v
    '--> 2 --> 3

Output: [0, 1, 1, 2]

Example 2:

Input: n = 3, edges = []
Output: [0, 0, 0]

Constraints:

    1 <= n <= 2000
    0 <= len(edges) <= 5000

    REQUIRED: must run in O(n + len(edges)) time.
"""


class Solution:

    def inDegrees(self, n: int, edges: List[List[int]]) -> List[int]:
        pass


sol = Solution()

print(sol.inDegrees(4, [[0, 1], [0, 2], [1, 3], [2, 3]]))  # [0, 1, 1, 2]

# assert sol.inDegrees(4, [[0, 1], [0, 2], [1, 3], [2, 3]]) == [0, 1, 1, 2]
# assert sol.inDegrees(3, []) == [0, 0, 0]
# assert sol.inDegrees(2, [[1, 0]]) == [1, 0]
# assert sol.inDegrees(3, [[2, 0], [0, 1], [1, 2]]) == [1, 1, 1]
