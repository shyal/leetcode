"""
URL: https://leetcode.com/problems/number-of-provinces/description/?envType=study-plan-v2&envId=leetcode-75

547. Number of Provinces

There are n cities. Some of them are connected, while some are not. If city a is connected directly with city b, and city b is connected directly with city c, then city a is connected indirectly with city c.

A province is a group of directly or indirectly connected cities and no other cities outside of the group.

You are given an n x n matrix isConnected where isConnected[i][j] = 1 if the ith city and the jth city are directly connected, and isConnected[i][j] = 0 otherwise.

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

from typing import List


class Solution:
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        def dfs(city):
            if city in seen:
                return 0
            seen.add(city)
            visited = 1
            for c in range(len(isConnected[city])):
                if isConnected[city][c]:
                    visited += dfs(c)
            return visited

        seen = set([])

        count = 0
        for i in range(len(isConnected)):
            visited = dfs(i)
            count += visited > 0

        return count


sol = Solution()
res = sol.findCircleNum([[1, 1, 0], [1, 1, 0], [0, 0, 1]])
assert res == 2


sol = Solution()
res = sol.findCircleNum([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
assert res == 3

assert sol.findCircleNum([[1]]) == 1
assert sol.findCircleNum([[1, 1], [1, 1]]) == 1
assert sol.findCircleNum([[1, 0], [0, 1]]) == 2
assert sol.findCircleNum([[1, 1, 1], [1, 1, 1], [1, 1, 1]]) == 1
assert sol.findCircleNum([[1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 1, 1], [0, 0, 1, 1]]) == 2
assert sol.findCircleNum([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]) == 4
assert sol.findCircleNum([[1, 1, 0], [1, 1, 1], [0, 1, 1]]) == 1
