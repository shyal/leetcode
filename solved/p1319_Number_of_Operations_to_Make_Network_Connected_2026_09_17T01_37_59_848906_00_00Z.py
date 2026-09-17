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
    No two computers are connected by more than onbute cable.

---

Ok this is a UF question, where we also have to carefully track
the number of disconnected networks, and the number of cables.


In example 1, there are 2 networks (N), and 3 cables (C).

The solution is 1, so presumably C - N.

In example 2:

N = 3
C = 5

C - N = 2

Which also tracks.

So we build the parent, write find and union, then count the networks
(e.g the unique roots). That's N.

Then it's simply a matter of len(connections) - N.



assert sol.makeConnected(6, [[0, 1], [0, 2], [0, 3], [1, 2]]) == -1

0  --  1
|  .  /
|   2
|
3


4      5      6

Assisted with this part:


spare = C - uc

if spare < N - 1:
    return -1
return N - 1

LEETCODE: Accepted (43 ms, 32.6 MB)
"""


class Solution:
    def makeConnected(self, n: int, connections: List[List[int]]) -> int:
        parent = [*range(n)]

        def find(x):
            while x != parent[x]:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a, b):
            pa = find(a)
            pb = find(b)
            if pa != pb:
                parent[pa] = pb
                return True
            return False

        C = len(connections)

        if C < n - 1:
            return -1

        uc = 0
        for a, b in connections:
            uc += union(a, b)

        N = len(set(find(x) for x in range(n)))
        spare = C - uc

        if spare < N - 1:
            return -1
        return N - 1


sol = Solution()

# print(sol.makeConnected(4, [[0, 1], [0, 2], [1, 2]]))  # 1

assert sol.makeConnected(4, [[0, 1], [0, 2], [1, 2]]) == 1
assert sol.makeConnected(6, [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3]]) == 2
assert sol.makeConnected(6, [[0, 1], [0, 2], [0, 3], [1, 2]]) == -1

assert sol.makeConnected(1, []) == 0
assert sol.makeConnected(2, [[0, 1]]) == 0
assert sol.makeConnected(2, []) == -1
assert sol.makeConnected(5, [[0, 1], [1, 2], [2, 3], [3, 4]]) == 0
assert sol.makeConnected(5, [[0, 1], [1, 2], [2, 3]]) == -1
assert sol.makeConnected(5, [[0, 1], [1, 2], [2, 3], [3, 4], [0, 2]]) == 0
assert sol.makeConnected(100000, [[i, i + 1] for i in range(99999)]) == 0
assert sol.makeConnected(100000, [[i, i + 1] for i in range(99998)]) == -1
assert sol.makeConnected(3, [[0, 1], [1, 2], [0, 2]]) == 0
assert sol.makeConnected(4, [[0, 1], [2, 3]]) == -1
assert sol.makeConnected(4, [[0, 1], [1, 2], [2, 3], [0, 2], [1, 3]]) == 0
assert sol.makeConnected(3, [[0, 1]]) == -1
