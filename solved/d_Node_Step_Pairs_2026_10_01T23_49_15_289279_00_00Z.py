"""
DRILL: Node Step Pairs

Start on node 0 of the directed graph G. Each step, move along one edge,
for at most k steps. For example, with G = {0: [1], 1: [2], 2: [3], 3: [1]}
and k = 4:

    0 -> 1 -> 2
         ^    |
         |    v
         +--- 3

we traverse as so: 0 -> 1 -> 2 -> 3 -> 1.

Return the traversal as a set of pairs (node_value, distance). The
node_value is the value of the node. The distance is how many steps you
have taken to get there, so node 1 appears as (1, 1) and as (1, 4).
When a node has several edges, follow every one of them.

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


# mu 0.7
# def reachable(G: {int: [int]}, k: int) -> {(int, int)}
#   q = deque([[0, 0]])
#   seen = set([(0, 0)])
#   while q
#     node, dist = q.popleft()
#     if dist > k
#       break
#     seen.add((node, dist))
#     for nxt in G[node]
#       pass
#       if (nxt, dist + 1) not in seen
#         q.append((nxt, dist + 1))
#   seen

class Solution:
    def reachable(self, G: dict[int, list[int]], k: int) -> set[tuple[int, int]]:
        q = deque([[0, 0]])
        seen = set([(0, 0)])
        while q:
            node, dist = q.popleft()
            if dist > k:
                break
            seen.add((node, dist))
            for nxt in G[node]:
                pass
                if (nxt, dist + 1) not in seen:
                    q.append((nxt, dist + 1))
        return seen


sol = Solution()
draw_graphviz({0: [1], 1: [2], 2: [3], 3: [1]}, type='directed')
print(sol.reachable({0: [1], 1: [2], 2: [3], 3: [1]}, 4))
assert sol.reachable({0: [1], 1: [2], 2: [3], 3: [1]}, 4) == {(0, 0), (1, 1), (1, 4), (2, 2), (3, 3)}
assert sol.reachable({0: [1], 1: [2], 2: [3], 3: [1]}, 0) == {(0, 0)}
assert sol.reachable({0: [1], 1: [2], 2: [3], 3: [1]}, 2) == {(0, 0), (1, 1), (2, 2)}
assert sol.reachable({0: [1, 2], 1: [2], 2: [0]}, 2) == {(0, 0), (0, 2), (1, 1), (2, 1), (2, 2)}
assert sol.reachable({0: [1], 1: [2], 2: []}, 3) == {(0, 0), (1, 1), (2, 2)}
assert sol.reachable({0: [1], 1: [1]}, 3) == {(0, 0), (1, 1), (1, 2), (1, 3)}
assert sol.reachable({0: []}, 5) == {(0, 0)}
assert sol.reachable({0: [1], 1: [0]}, 3) == {(0, 0), (0, 2), (1, 1), (1, 3)}
assert sol.reachable({0: [1, 2], 1: [3], 2: [3], 3: []}, 2) == {(0, 0), (1, 1), (2, 1), (3, 2)}
assert sol.reachable({0: [0]}, 2) == {(0, 0), (0, 1), (0, 2)}
assert sol.reachable({0: [], 1: [2], 2: [1]}, 2) == {(0, 0)}
