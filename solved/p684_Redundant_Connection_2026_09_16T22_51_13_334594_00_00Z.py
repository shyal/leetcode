"""
URL: https://leetcode.com/problems/redundant-connection/description/?envType=problem-list-v2&envId=vn57k9wr

684. Redundant Connection

In this problem, a tree is an undirected graph that is connected and has no cycles.

You are given a graph that started as a tree with n nodes labeled from 1 to n, with one additional edge added. The added edge has two different vertices chosen from 1 to n, and was not an edge that already existed. The graph is represented as an array edges of length n where edges[i] = [a_i, b_i] indicates that there is an edge between nodes a_i and b_i in the graph.

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
    1 <= a_i < b_i <= edges.length
    a_i != b_i
    There are no repeated edges.
    The given graph is connected.

---

LEETCODE: Runtime Error (Line 28: IndexError: list index out of range)
"""


class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        parent = defaultdict(int)
        for a, b in edges:
            parent[a] = a
            parent[b] = b

        def find(x):
            if parent[x] == x:
                return x
            return find(parent[x])

        def union(a, b):
            pa = find(a)
            pb = find(b)
            if pa != pb:
                parent[a] = pb
                return True
            else:
                return False

        res = []
        for a, b in edges:
            u = union(b, a)
            if not u:
                res.append([a, b])

        return res[-1]


sol = Solution()

print(sol.findRedundantConnection([[1, 2], [1, 3], [2, 3]]))  # [2,3]

assert sol.findRedundantConnection([[1, 2], [1, 3], [2, 3]]) == [2, 3]
assert sol.findRedundantConnection([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]) == [1, 4]

assert Solution().findRedundantConnection([[1, 2], [2, 3], [3, 1]]) == [3, 1]
assert Solution().findRedundantConnection([[1, 2], [2, 3], [3, 4], [4, 5], [5, 1]]) == [
    5,
    1,
]
assert Solution().findRedundantConnection(
    [[1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], [9, 10], [10, 1]]
) == [10, 1]
assert Solution().findRedundantConnection(
    [
        [1, 2],
        [2, 3],
        [3, 4],
        [4, 5],
        [5, 6],
        [6, 7],
        [7, 8],
        [8, 9],
        [9, 10],
        [10, 11],
        [11, 12],
        [12, 1],
    ]
) == [12, 1]
assert Solution().findRedundantConnection(
    [
        [1, 2],
        [2, 3],
        [3, 4],
        [4, 5],
        [5, 6],
        [6, 7],
        [7, 8],
        [8, 9],
        [9, 10],
        [10, 11],
        [11, 12],
        [12, 13],
        [13, 1],
    ]
) == [13, 1]
assert Solution().findRedundantConnection(
    [
        [1, 2],
        [2, 3],
        [3, 4],
        [4, 5],
        [5, 6],
        [6, 7],
        [7, 8],
        [8, 9],
        [9, 10],
        [10, 11],
        [11, 12],
        [12, 13],
        [13, 14],
        [14, 1],
    ]
) == [14, 1]
assert Solution().findRedundantConnection(
    [
        [1, 2],
        [2, 3],
        [3, 4],
        [4, 5],
        [5, 6],
        [6, 7],
        [7, 8],
        [8, 9],
        [9, 10],
        [10, 11],
        [11, 12],
        [12, 13],
        [13, 14],
        [14, 15],
        [15, 1],
    ]
) == [15, 1]
assert Solution().findRedundantConnection(
    [
        [1, 2],
        [2, 3],
        [3, 4],
        [4, 5],
        [5, 6],
        [6, 7],
        [7, 8],
        [8, 9],
        [9, 10],
        [10, 11],
        [11, 12],
        [12, 13],
        [13, 14],
        [14, 15],
        [15, 16],
        [16, 1],
    ]
) == [16, 1]
assert Solution().findRedundantConnection(
    [
        [1, 2],
        [2, 3],
        [3, 4],
        [4, 5],
        [5, 6],
        [6, 7],
        [7, 8],
        [8, 9],
        [9, 10],
        [10, 11],
        [11, 12],
        [12, 13],
        [13, 14],
        [14, 15],
        [15, 16],
        [16, 17],
        [17, 1],
    ]
) == [17, 1]
assert Solution().findRedundantConnection(
    [
        [1, 2],
        [2, 3],
        [3, 4],
        [4, 5],
        [5, 6],
        [6, 7],
        [7, 8],
        [8, 9],
        [9, 10],
        [10, 11],
        [11, 12],
        [12, 13],
        [13, 14],
        [14, 15],
        [15, 16],
        [16, 17],
        [17, 18],
        [18, 1],
    ]
) == [18, 1]
assert Solution().findRedundantConnection(
    [
        [1, 2],
        [2, 3],
        [3, 4],
        [4, 5],
        [5, 6],
        [6, 7],
        [7, 8],
        [8, 9],
        [9, 10],
        [10, 11],
        [11, 12],
        [12, 13],
        [13, 14],
        [14, 15],
        [15, 16],
        [16, 17],
        [17, 18],
        [18, 19],
        [19, 1],
    ]
) == [19, 1]
assert Solution().findRedundantConnection(
    [
        [1, 2],
        [2, 3],
        [3, 4],
        [4, 5],
        [5, 6],
        [6, 7],
        [7, 8],
        [8, 9],
        [9, 10],
        [10, 11],
        [11, 12],
        [12, 13],
        [13, 14],
        [14, 15],
        [15, 16],
        [16, 17],
        [17, 18],
        [18, 19],
        [19, 20],
        [20, 1],
    ]
) == [20, 1]
