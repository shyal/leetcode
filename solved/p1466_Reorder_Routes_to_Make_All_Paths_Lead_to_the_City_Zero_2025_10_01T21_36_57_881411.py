"""
URL: https://leetcode.com/problems/reorder-routes-to-make-all-paths-lead-to-the-city-zero/description/?envType=study-plan-v2&envId=leetcode-75

1466. Reorder Routes to Make All Paths Lead to the City Zero

There are n cities numbered from 0 to n - 1 and n - 1 roads such that there is only one way to travel between two different cities (this network form a tree). Last year, The ministry of transport decided to orient the roads in one direction because they are too narrow.

Roads are represented by connections where connections[i] = [ai, bi] represents a road from city ai to city bi.

This year, there will be a big event in the capital (city 0), and many people want to travel to this city.

Your task consists of reorienting some roads such that each city can visit the city 0. Return the minimum number of edges changed.

It's guaranteed that each city can reach city 0 after reorder.


Example 1:

Input: n = 6, connections = [[0,1],[1,3],[2,3],[4,0],[4,5]]
Output: 3
Explanation: Change the direction of edges show in red such that each node can reach the node 0 (capital).

Example 2:

Input: n = 5, connections = [[1,0],[1,2],[3,2],[3,4]]
Output: 2
Explanation: Change the direction of edges show in red such that each node can reach the node 0 (capital).

Example 3:

Input: n = 3, connections = [[1,0],[2,0]]
Output: 0


Constraints:

        2 <= n <= 5 * 104
        connections.length == n - 1
        connections[i].length == 2
        0 <= ai, bi <= n - 1
        ai != bi
"""

from typing import List
from collections import defaultdict


class Solution:
    def minReorder(self, n: int, connections: List[List[int]]) -> int:
        def dfs(city):
            seen.add(city)
            neighbouring_cities = G[city].keys()
            flips = 0
            for neighbouring_city in neighbouring_cities:
                if neighbouring_city in seen:
                    continue
                if G[city][neighbouring_city] == 1:
                    flips += 1
                flips += dfs(neighbouring_city)
            return flips

        seen = set([])
        G = defaultdict(dict)
        for c1, c2 in connections:
            G[c1][c2] = 1
            G[c2][c1] = 0

        return dfs(0)


sol = Solution()

res = sol.minReorder(n=6, connections=[[0, 1], [1, 3], [2, 3], [4, 0], [4, 5]])
assert res == 3

res = sol.minReorder(n=5, connections=[[1, 0], [1, 2], [3, 2], [3, 4]])
assert res == 2

res = sol.minReorder(n=3, connections=[[1, 0], [2, 0]])
assert res == 0

res = sol.minReorder(2, [[0, 1]])
assert res == 1

res = sol.minReorder(2, [[1, 0]])
assert res == 0

res = sol.minReorder(4, [[0, 1], [0, 2], [0, 3]])
assert res == 3

res = sol.minReorder(4, [[1, 0], [2, 0], [3, 0]])
assert res == 0

res = sol.minReorder(4, [[0, 1], [1, 2], [3, 2]])
assert res == 2

res = sol.minReorder(5, [[0, 1], [1, 2], [1, 3], [1, 4]])
assert res == 4

res = sol.minReorder(5, [[1, 0], [2, 1], [3, 1], [4, 1]])
assert res == 0

res = sol.minReorder(7, [[0, 1], [1, 2], [2, 3], [0, 4], [4, 5], [4, 6]])
assert res == 6

res = sol.minReorder(7, [[0, 1], [1, 2], [3, 2], [0, 4], [4, 5], [6, 4]])
assert res == 4

