"""
URL: https://leetcode.com/problems/number-of-provinces/description/?envType=problem-list-v2&envId=vn57k9wr

547. Number of Provinces

There are n cities. Some of them are connected, while some are not. If city a
is connected directly with city b, and city b is connected directly with city
c, then city a is connected indirectly with city c.

A province is a group of directly or indirectly connected cities and no other
cities outside of the group.

You are given an n x n matrix isConnected where isConnected[i][j] = 1 if the
ith city and the jth city are directly connected, and isConnected[i][j] = 0
otherwise.

Return the total number of provinces.


Example 1:

Input: isConnected = [[1,1,0],[1,1,0],[0,0,1]]
Output: 2

Example 2:

Input: isConnected = [[1,0,0],[0,1,0],[0,0,1]]
Output: 3


Constraints:

    1 <= n <= 200
    n == isConnected.length
    n == isConnected[i].length
    isConnected[i][j] is 1 or 0.
    isConnected[i][i] == 1
    isConnected[i][j] == isConnected[j][i]
"""


class Solution:
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        def helper(i):
            if i in visited:
                return
            visited.add(i)
            for j in range(len(isConnected[i])):
                if i != j:
                    if isConnected[i][j]:
                        helper(j)

        count = 0
        visited = set([])
        for i in range(len(isConnected)):
            if i not in visited:
                count += 1
                helper(i)
        return count


sol = Solution()

assert sol.findCircleNum([[1, 1, 0], [1, 1, 0], [0, 0, 1]]) == 2
assert sol.findCircleNum([[1, 0, 0], [0, 1, 0], [0, 0, 1]]) == 3
assert sol.findCircleNum([[1]]) == 1
assert sol.findCircleNum([[1, 0], [0, 1]]) == 2
assert sol.findCircleNum([[1, 1], [1, 1]]) == 1
assert sol.findCircleNum([[1, 1, 1], [1, 1, 1], [1, 1, 1]]) == 1
assert sol.findCircleNum([[1, 1, 0], [1, 1, 1], [0, 1, 1]]) == 1
assert sol.findCircleNum([[1, 1, 0, 0], [1, 1, 1, 0], [0, 1, 1, 1], [0, 0, 1, 1]]) == 1
assert sol.findCircleNum([[1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 1, 1], [0, 0, 1, 1]]) == 2
assert sol.findCircleNum([[1, 0, 0, 1], [0, 1, 1, 0], [0, 1, 1, 0], [1, 0, 0, 1]]) == 2
assert sol.findCircleNum([[1, 1, 1, 1], [1, 1, 0, 0], [1, 0, 1, 0], [1, 0, 0, 1]]) == 1
assert (
    sol.findCircleNum(
        [
            [1, 1, 0, 0, 0],
            [1, 1, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 1, 1],
            [0, 0, 0, 1, 1],
        ]
    )
    == 3
)
assert (
    sol.findCircleNum(
        [
            [1, 0, 0, 0, 1],
            [0, 1, 0, 0, 0],
            [0, 0, 1, 1, 0],
            [0, 0, 1, 1, 0],
            [1, 0, 0, 0, 1],
        ]
    )
    == 3
)
assert (
    sol.findCircleNum([[1 if i == j else 0 for j in range(200)] for i in range(200)])
    == 200
)
assert sol.findCircleNum([[1] * 200 for _ in range(200)]) == 1
assert (
    sol.findCircleNum(
        [[1 if abs(i - j) <= 1 else 0 for j in range(200)] for i in range(200)]
    )
    == 1
)