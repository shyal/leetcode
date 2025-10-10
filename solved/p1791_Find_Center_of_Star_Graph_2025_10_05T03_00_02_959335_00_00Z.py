"""
URL: https://leetcode.com/problems/find-center-of-star-graph/description/

1791. Find Center of Star Graph

There is an undirected star graph consisting of n nodes labeled from 1 to n. A star graph is a graph where there is one center node and exactly n - 1 edges that connect the center node with every other node.

You are given a 2D integer array edges where each edges[i] = [ui, vi] indicates that there is an edge between the nodes ui and vi. Return the center of the given star graph.


Example 1:

Input: edges = [[1,2],[2,3],[4,2]]
Output: 2
Explanation: As shown in the figure above, node 2 is connected to every other node, so 2 is the center.

Example 2:

Input: edges = [[1,2],[5,1],[1,3],[1,4]]
Output: 1


Constraints:

    3 <= n <= 10^5
    edges.length == n - 1
    1 <= ui, vi <= n
    ui != vi
    The given edges form a valid star graph.
"""


class Solution:
    def findCenter(self, edges: List[List[int]]) -> int:
        s = set(edges[0])
        for i in range(1, len(edges)):
            s.intersection_update(edges[i])
        return next(iter(s))


sol = Solution()

assert sol.findCenter([[1, 2], [2, 3], [4, 2]]) == 2
assert sol.findCenter([[1, 2], [5, 1], [1, 3], [1, 4]]) == 1
assert sol.findCenter([[1, 2], [1, 3]]) == 1
assert sol.findCenter([[2, 1], [2, 3]]) == 2
assert sol.findCenter([[1, 2], [3, 2]]) == 2
assert sol.findCenter([[1, 3], [2, 3]]) == 3
assert sol.findCenter([[4, 1], [4, 2], [4, 3]]) == 4
assert sol.findCenter([[4, 1], [2, 4]]) == 4
assert sol.findCenter([[1, 2], [2, 3], [2, 4], [2, 5]]) == 2
