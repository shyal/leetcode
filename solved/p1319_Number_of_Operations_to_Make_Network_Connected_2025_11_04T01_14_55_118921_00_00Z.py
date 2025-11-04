"""
URL: https://leetcode.com/problems/number-of-operations-to-make-network-connected/description/?envType=problem-list-v2&envId=vn57k9wr

1319. Number of Operations to Make Network Connected

There are n computers numbered from 0 to n - 1 connected by ethernet cables connections forming a network where connections[i] = [ai, bi] represents a connection between computers ai and bi. Any computer can reach any other computer directly or indirectly through the network.

You are given an initial computer network connections. You can extract certain cables between two directly connected computers, and place them between any pair of disconnected computers to make them directly connected.

Return the minimum number of times you need to do this in order to make all the computers connected. If it is not possible, return -1.

Example 1:

Input: n = 4, connections = [[0,1],[0,2],[1,2]]
Output: 1
Explanation: Remove cable between computer 1 and 2 and place between computers 1 and 3.

Example 2:

Input: n = 6, connections = [[0,1],[0,2],[0,3],[1,2],[1,3]]
Output: 2

Example 3:

Input: n = 6, connections = [[0,1],[0,2],[0,3],[1,2]]
Output: -1
Explanation: There are not enough cables.

Constraints:

    1 <= n <= 10^5
    1 <= connections.length <= min(n * (n - 1) / 2, 10^5)
    connections[i].length == 2
    0 <= ai, bi < n
    ai != bi
    There are no repeated connections.
    No two computers are connected by more than one cable.

---

Revisiting as i didn't successfully solve this last time. So the key insight in this solve, is that
we can count the number of disjoint sets with self.count = n, and decrementing it each time
we merge two sets. Great!

"""


class Solution:

    def makeConnected(self, n: int, connections: List[List[int]]) -> int:
        parent = list(range(n))
        self.num_networks = n
        self.redundant_cables = 0

        def find(x):
            if x != parent[x]:
                parent[x] = find(parent[x])
            return parent[x]

        def union(x, y):
            rootx = find(x)
            rooty = find(y)
            if rootx != rooty:
                parent[rootx] = rooty
                self.num_networks -= 1
            else:
                self.redundant_cables += 1

        for x, y in connections:
            union(x, y)

        # print("redundant", self.redundant_cables)
        # print("count", self.num_networks)

        if self.redundant_cables >= self.num_networks - 1:
            return self.num_networks - 1
        else:
            return -1


sol = Solution()

edges = [[0, 1], [0, 2], [1, 2]]
draw_graphviz(edges)

# print(sol.makeConnected(4, edges))  # 1


edges = [[0, 1], [0, 2], [1, 2]]
draw_graphviz(edges, n=4)
sol.makeConnected(4, edges) == 1

edges = [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3]]
draw_graphviz(edges, n=6)
sol.makeConnected(6, edges) == 2

edges = []
draw_graphviz(edges, n=1)
sol.makeConnected(1, edges) == 0

edges = [[0, 1]]
draw_graphviz(edges, n=2)
sol.makeConnected(2, edges) == 0

edges = [[0, 1], [0, 2]]
draw_graphviz(edges, n=3)
sol.makeConnected(3, edges) == 0

edges = [[0, 1], [1, 2], [0, 2]]
draw_graphviz(edges, n=3)
sol.makeConnected(3, edges) == 0

edges = [[0, 1], [0, 2], [0, 3], [0, 4]]
draw_graphviz(edges, n=5)
sol.makeConnected(5, edges) == 0

edges = [[0, 1], [0, 2], [1, 2], [3, 4]]
draw_graphviz(edges, n=5)
sol.makeConnected(5, edges) == 1

edges = [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]]
draw_graphviz(edges, n=5)
sol.makeConnected(5, edges) == 1

edges = [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [4, 5], [4, 6]]
draw_graphviz(edges, n=7)
sol.makeConnected(7, edges) == 1

edges = [[1, 2], [1, 3], [1, 4], [2, 3]]
draw_graphviz(edges, n=5)
sol.makeConnected(5, edges) == 1

edges = [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [4, 5]]
draw_graphviz(edges, n=6)
sol.makeConnected(6, edges) == 1

edges = [[0, 1], [0, 3], [0, 4], [1, 3]]
draw_graphviz(edges, n=5)
sol.makeConnected(5, edges) == 1

edges = []
draw_graphviz(edges, n=2)
sol.makeConnected(2, edges) == -1

edges = [[0, 1]]
draw_graphviz(edges, n=3)
sol.makeConnected(3, edges) == -1

edges = [[0, 1], [2, 3]]
draw_graphviz(edges, n=5)
sol.makeConnected(5, edges) == -1

edges = []
draw_graphviz(edges, n=4)
sol.makeConnected(4, edges) == -1

edges = [[0, 2]]
draw_graphviz(edges, n=3)
sol.makeConnected(3, edges) == -1

edges = [[0, 2], [0, 3]]
draw_graphviz(edges, n=4)
sol.makeConnected(4, edges) == -1

edges = [[0, 1], [0, 2], [0, 3], [1, 2]]
draw_graphviz(edges, n=6)
sol.makeConnected(6, edges) == -1

edges = [[2, 3], [3, 4]]
draw_graphviz(edges, n=5)
sol.makeConnected(5, edges) == -1
