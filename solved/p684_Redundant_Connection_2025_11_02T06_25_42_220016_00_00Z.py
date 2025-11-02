"""
URL: https://leetcode.com/problems/redundant-connection/description/?envType=problem-list-v2&envId=vn57k9wr

684. Redundant Connection

In this problem, a tree is an undirected graph that is connected and has no cycles.

You are given a graph that started as a tree with n nodes labeled from 1 to n, with one additional edge added. The added edge has two different vertices chosen from 1 to n, and was not an edge that already existed. The graph is represented as an array edges of length n where edges[i] = [ai, bi] indicates that there is an edge between nodes ai and bi in the graph.

Return an edge that can be removed so that the resulting graph is a tree of n nodes. If there are multiple answers, return the answer that occurs last in the input.

Example 1:

Input: edges = [[1,2],[1,3],[2,3]]
Output: [2,3]

Example 2:

Input: edges = [[1,2],[2,3],[3,4],[1,4],[1,5]]
Output: [1,4]

Constraints:

    n == edges.length
    3 <= n <= 1000
    edges[i].length == 2
    1 <= ai < bi <= edges.length
    ai != bi
    There are no repeated edges.
    The given graph is connected.

---

Once you know union find, solving this problem is trivial.

"""


class Solution:

    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        parents = [x for x in range(len(edges) + 1)]

        def find(x):
            if x != parents[x]:
                parents[x] = find(parents[x])
            return parents[x]

        def union(x, y):
            rootx = find(x)
            rooty = find(y)
            if rootx != rooty:
                parents[rootx] = rooty

        dupe = []
        for x, y in edges:
            rootx = find(x)
            rooty = find(y)
            if rootx == rooty:
                dupe.append([x, y])
            union(x, y)
        return dupe[-1]


sol = Solution()
assert sol.findRedundantConnection([[1, 2], [1, 3], [2, 3]]) == [2, 3]
assert sol.findRedundantConnection([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]) == [1, 4]
assert sol.findRedundantConnection([[1, 2], [2, 3], [1, 3]]) == [1, 3]
assert sol.findRedundantConnection([[1, 3], [2, 3], [1, 2]]) == [1, 2]
assert sol.findRedundantConnection([[1, 2], [3, 4], [1, 3], [2, 4]]) == [2, 4]
assert sol.findRedundantConnection([[1, 2], [2, 3], [3, 4], [4, 5], [1, 5]]) == [1, 5]
assert sol.findRedundantConnection([[1, 2], [1, 3], [2, 4], [3, 4]]) == [3, 4]
