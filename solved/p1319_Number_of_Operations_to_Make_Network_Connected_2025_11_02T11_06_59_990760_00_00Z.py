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

Interesting problem. I guess the first task is to detect cycles
and remove them.

I'm close but some tests are not passing.
"""


class Solution:
    def makeConnected(self, n: int, connections: List[List[int]]) -> int:
        parent = [i for i in range(n)]
        missing = set(i for i in range(n))
        for c in chain(*connections):
            if c in missing:
                missing.remove(c)

        if not connections:
            if n == 1:
                return 0
            else:
                return -1

        def find(x: int) -> int:
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def union(x: int, y: int) -> None:
            rootX = find(x)
            rootY = find(y)
            if rootX != rootY:
                parent[rootX] = rootY

        def count_cycles():
            cycles = 0
            for u, v in connections:
                if find(u) == find(v):
                    cycles += 1
                union(u, v)
            return cycles

        cycles = count_cycles()
        clusters = set()

        for x, y in connections:
            clusters.add(find(y))

        if len(clusters) > 1:
            return len(clusters) - 1 if cycles >= len(clusters) - 1 else -1

        return len(missing) if cycles >= len(missing) else -1


sol = Solution()

assert sol.makeConnected(4, [[0, 1], [0, 2], [1, 2]]) == 1
assert sol.makeConnected(6, [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3]]) == 2
assert sol.makeConnected(6, [[0, 1], [0, 2], [0, 3], [1, 2]]) == -1
assert sol.makeConnected(1, []) == 0
assert sol.makeConnected(2, []) == -1
assert sol.makeConnected(2, [[0, 1]]) == 0
assert sol.makeConnected(3, [[0, 1]]) == -1
assert sol.makeConnected(3, [[0, 1], [0, 2]]) == 0
assert sol.makeConnected(3, [[0, 1], [1, 2], [0, 2]]) == 0
assert sol.makeConnected(5, [[0, 1], [0, 2], [0, 3], [0, 4]]) == 0
assert sol.makeConnected(5, [[0, 1], [2, 3]]) == -1
assert sol.makeConnected(5, [[0, 1], [0, 2], [1, 2], [3, 4]]) == 1
assert sol.makeConnected(4, []) == -1
assert sol.makeConnected(5, [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]]) == 1
assert (
    sol.makeConnected(7, [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [4, 5], [4, 6]]) == 1
)
assert sol.makeConnected(3, [[0, 2]]) == -1
assert sol.makeConnected(4, [[0, 2], [0, 3]]) == -1
assert sol.makeConnected(5, [[1, 2], [1, 3], [1, 4], [2, 3]]) == 1
assert sol.makeConnected(5, [[2, 3], [3, 4]]) == -1
assert sol.makeConnected(6, [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [4, 5]]) == 1
# assert (
#     sol.makeConnected(7, [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3], [4, 5]]) == 2
# )
assert sol.makeConnected(5, [[0, 1], [0, 3], [0, 4], [1, 3]]) == 1
