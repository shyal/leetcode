"""
URL: https://leetcode.com/problems/number-of-operations-to-make-network-connected/description/?envType=problem-list-v2&envId=vn57k9wr

1319. Number of Operations to Make Network Connected

There are n computers numbered from 0 to n - 1 connected by ethernet cables connections forming a network where connections[i] = [a_i, b_i] represents a connection between computers a_i and b_i. Any computer can reach any other computer directly or indirectly through the network.

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
    0 <= a_i, b_i < n
    a_i != b_i
    There are no repeated connections.
    No two computers are connected by more than one cable.

---

I got hinted for:

if len(connections) < n - 1:
    return -1

groups = sum(1 for k in range(n) if find(k) == k)

"""


class Solution:
    def makeConnected(self, n: int, connections: List[List[int]]) -> int:

        parent = [*range(n)]

        def find(x):
            if x != parent[x]:
                parent[x] = find(parent[x])
            return parent[x]

        def union(a, b):
            pa = find(a)
            pb = find(b)
            if pa != pb:
                parent[pa] = pb
                return True
            return False

        count = 0
        for a, b in connections:
            count += int(union(a, b))

        if len(connections) < n - 1:
            return -1

        groups = sum(1 for k in range(n) if find(k) == k)
        return groups - 1


sol = Solution()

print(sol.makeConnected(4, [[0, 1], [0, 2], [1, 2]]))  # 1

assert sol.makeConnected(4, [[0, 1], [0, 2], [1, 2]]) == 1
assert sol.makeConnected(6, [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3]]) == 2
assert sol.makeConnected(6, [[0, 1], [0, 2], [0, 3], [1, 2]]) == -1

assert sol.makeConnected(1, []) == 0
assert sol.makeConnected(2, [[0, 1]]) == 0
assert sol.makeConnected(2, []) == -1
assert sol.makeConnected(5, [[0, 1], [1, 2], [2, 3], [3, 4]]) == 0
assert sol.makeConnected(5, [[0, 1], [1, 2], [2, 3]]) == -1
assert sol.makeConnected(5, [[0, 1], [1, 2], [2, 3], [3, 4], [0, 2]]) == 0
# assert sol.makeConnected(100000, [[i, i + 1] for i in range(99999)]) == 0
# assert sol.makeConnected(100000, [[i, i + 1] for i in range(99998)]) == -1
assert sol.makeConnected(3, [[0, 1], [1, 2], [0, 2]]) == 0
assert sol.makeConnected(4, [[0, 1], [2, 3]]) == -1
assert sol.makeConnected(4, [[0, 1], [1, 2], [2, 3], [0, 2], [1, 3]]) == 0
assert sol.makeConnected(3, [[0, 1]]) == -1
