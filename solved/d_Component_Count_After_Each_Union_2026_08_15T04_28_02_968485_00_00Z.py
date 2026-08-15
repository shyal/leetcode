"""
DRILL: Component Count After Each Union
TRAINS: union-find

Given n nodes labeled 0..n-1 and a list of undirected edges, process the
edges in order and return a list where res[i] is the number of connected
components after processing edges[0..i].

An edge between two already-connected nodes changes nothing — the count
stays flat.

Example 1:

Input: n = 4, edges = [[0,1],[0,2],[1,2]]
Output: [3, 2, 2]
Explanation:
    [0,1] -> {0,1} {2} {3}        -> 3 components
    [0,2] -> {0,1,2} {3}          -> 2 components
    [1,2] -> already connected    -> still 2

    0
   / \\
  1---2      3

Triangle 0-1-2, node 3 alone.

Example 2:

Input: n = 3, edges = [[0,1],[1,2]]
Output: [2, 1]

  0---1---2

A chain, all one component.

Constraints:

    1 <= n <= 1000
    0 <= len(edges) <= 2000
    0 <= u, v < n

    REQUIRED: union-find (parent array + find + union), not BFS/DFS.
    find compresses the path; union links root to root.

---

Hints given:

1. Create a list parent containing [0...i]. Those are the "parents" for each node. Right now, each node is its own parent.
2. Write a function find(x): look at parent[x]. If it equals x, x is a root, return x. If not, hop: repeat the same check on parent[x] instead. Keep hopping until the node you're on is its own parent.
3. Write a function union(a, b): call find(a) and find(b) to get the two roots, call them ra and rb. If ra equals rb, the nodes are already in the same group — return False. Otherwise set parent[ra] = rb (root ra now hangs under root rb) and return True.
4. Set count = n and res = [] (empty list). Loop over the edges: for each edge, call union on its two nodes. If union returned True, subtract 1 from count. Either way, append the current count to res. After the loop, return res.
"""


class Solution:
    def componentCounts(self, n: int, edges: list[list[int]]) -> list[int]:
        # Create a list parent containing [0...i]. Those are the "parents" for each node. Right now, each node is its own parent.
        parent = [*range(n)]

        # Write a function find(x): look at parent[x]. If it equals x, x is a root, return x. If not,
        # hop: repeat the same check on parent[x] instead. Keep hopping until the node you're on is its own parent.
        def find(x):
            if parent[x] == x:
                return x
            else:
                return find(parent[x])

        # Write a function union(a, b): call find(a) and find(b) to get the two roots, call them ra and rb. 
        # If ra equals rb, the nodes are already in the same group — return False. Otherwise set parent[ra] = rb (root ra now hangs under root rb) and return True.
        def union(a, b):
            ra = find(a)
            rb = find(b)
            if ra == rb:
                return False
            else:
                parent[ra] = rb
                return True

        # Set count = n and res = [] (empty list). Loop over the edges: for each edge, call union on its two nodes.
        # If union returned True, subtract 1 from count. Either way, append the current count to res. After the loop, return res.
        count = n
        res = []
        for a, b in edges:
            if union(a, b):
                count -= 1
            res.append(count)
        return res


sol = Solution()

assert sol.componentCounts(4, [[0, 1], [0, 2], [1, 2]]) == [3, 2, 2]
assert sol.componentCounts(3, [[0, 1], [1, 2]]) == [2, 1]
assert sol.componentCounts(5, []) == []
assert sol.componentCounts(6, [[0, 1], [2, 3], [4, 5], [0, 2], [3, 5]]) == [5, 4, 3, 2, 1]
assert sol.componentCounts(4, [[0, 1], [1, 0], [2, 3], [0, 3]]) == [3, 3, 2, 1]
assert sol.componentCounts(1, []) == []
assert sol.componentCounts(2, [[0, 1], [0, 1]]) == [1, 1]

print("All tests passed!")
