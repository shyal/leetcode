"""
DRILL: Node Step Pairs

Given a dict G from each node of a directed graph to the list of nodes
its edges point to, and an integer k, return the set of pairs (x, d)
such that a path of exactly d edges from node 0 reaches node x, for
every d from 0 to k. A path may repeat nodes and edges. The pair (0, 0)
is always in the set.

Example 1:

Input: G = {0: [1], 1: [2], 2: [3], 3: [1]}, k = 4
Output: {(0, 0), (1, 1), (2, 2), (3, 3), (1, 4)}

    0 -> 1 -> 2
         ^    |
         |    v
         +--- 3

Explanation: The path 0 -> 1 -> 2 -> 3 -> 1 reaches node 1 a second
time, with 4 edges.

Example 2:

Input: G = {0: [1, 2], 1: [2], 2: [0]}, k = 2
Output: {(0, 0), (1, 1), (2, 1), (2, 2), (0, 2)}

    0 ---> 1
    ^ \    |
    |  \   |
    |   v  v
    +----- 2

Example 3:

Input: G = {0: [1], 1: [2], 2: []}, k = 3
Output: {(0, 0), (1, 1), (2, 2)}

    0 -> 1 -> 2

Constraints:

    1 <= len(G) <= 100
    0 <= k <= 100

    REQUIRED: O(k * (n + m)), one breadth-first search from node 0. A
    visited set keyed on the node alone drops (1, 4) from Example 1.
"""


class Solution:

    def reachable(self, G: Dict[int, List[int]], k: int) -> set[tuple[int, int]]:
        pass


sol = Solution()

draw_graphviz({0: [1], 1: [2], 2: [3], 3: [1]}, type="directed")
print(
    sol.reachable({0: [1], 1: [2], 2: [3], 3: [1]}, 4)
)  # {(0, 0), (1, 1), (2, 2), (3, 3), (1, 4)}

# assert sol.reachable({0: [1], 1: [2], 2: [3], 3: [1]}, 4) == {(0, 0), (1, 1), (1, 4), (2, 2), (3, 3)}
# assert sol.reachable({0: [1], 1: [2], 2: [3], 3: [1]}, 0) == {(0, 0)}
# assert sol.reachable({0: [1], 1: [2], 2: [3], 3: [1]}, 2) == {(0, 0), (1, 1), (2, 2)}
# assert sol.reachable({0: [1, 2], 1: [2], 2: [0]}, 2) == {(0, 0), (0, 2), (1, 1), (2, 1), (2, 2)}
# assert sol.reachable({0: [1], 1: [2], 2: []}, 3) == {(0, 0), (1, 1), (2, 2)}
# assert sol.reachable({0: [1], 1: [1]}, 3) == {(0, 0), (1, 1), (1, 2), (1, 3)}
# assert sol.reachable({0: []}, 5) == {(0, 0)}
# assert sol.reachable({0: [1], 1: [0]}, 3) == {(0, 0), (0, 2), (1, 1), (1, 3)}
# assert sol.reachable({0: [1, 2], 1: [3], 2: [3], 3: []}, 2) == {(0, 0), (1, 1), (2, 1), (3, 2)}
# assert sol.reachable({0: [0]}, 2) == {(0, 0), (0, 1), (0, 2)}
# assert sol.reachable({0: [], 1: [2], 2: [1]}, 2) == {(0, 0)}
