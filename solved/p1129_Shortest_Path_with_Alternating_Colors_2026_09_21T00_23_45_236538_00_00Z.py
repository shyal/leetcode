"""
URL: https://leetcode.com/problems/shortest-path-with-alternating-colors/description/?envType=problem-list-v2&envId=vn57k9wr

1129. Shortest Path with Alternating Colors

You are given an integer n, the number of nodes in a directed graph where the nodes are labeled from 0 to n - 1. Each edge is red or blue in this graph, and there could be self-edges and parallel edges.

You are given two arrays redEdges and blueEdges where:

- redEdges[i] = [a_i, b_i] indicates that there is a directed red edge from node a_i to node b_i in the graph, and
- blueEdges[j] = [u_j, v_j] indicates that there is a directed blue edge from node u_j to node v_j in the graph.

Return an array answer of length n, where each answer[x] is the length of the shortest path from node 0 to node x such that the edge colors alternate along the path, or -1 if such a path does not exist.

Example 1:

Input: n = 3, redEdges = [[0,1],[1,2]], blueEdges = []
Output: [0,1,-1]

Example 2:

Input: n = 3, redEdges = [[0,1]], blueEdges = [[2,1]]
Output: [0,1,-1]

Constraints:

    1 <= n <= 100
    0 <= redEdges.length, blueEdges.length <= 400
    redEdges[i].length == blueEdges[j].length == 2
    0 <= a_i, b_i, u_j, v_j < n

---



Passes 24 test cases. Not sure why some are not passing.

Giving up.

LEETCODE: Wrong Answer (28/91 cases)
"""


class Solution:
    def shortestAlternatingPaths(
        self, n: int, redEdges: List[List[int]], blueEdges: List[List[int]]
    ) -> List[int]:
        G = defaultdict(list)
        for i in range(n):
            G[i]
        for a, b in redEdges:
            G[a].append([b, "red"])
        for a, b in blueEdges:
            G[a].append([b, "blue"])
        # print(G)

        def bfs(target_node=1, origin_node=0):
            q = deque([[origin_node, 0, []]])
            while q:
                n, dist, col = q.popleft()
                if dist > n:
                    break
                if n == target_node:
                    if answer[target_node] == -1:
                        good = True
                        prev = None
                        for c in col:
                            if prev:
                                good = good and c != prev
                            prev = c
                        answer[target_node] = dist if good else -1
                        return
                for children in G[n]:
                    nxt, nextcol = children
                    q.append([nxt, dist + 1, col + [nextcol]])

        answer = table(n, fill=-1)
        # bfs(target_node=1)
        for i in range(n):
            bfs(target_node=i)
        print(answer)
        return answer


sol = Solution()


# assert Solution().shortestAlternatingPaths(
#     3, [[0, 1], [0, 1], [1, 2]], [[0, 1], [1, 2], [1, 2]]
# ) == [0, 1, 2]

# print(sol.shortestAlternatingPaths(3, [[0, 1], [1, 2]], []))  # [0,1,-1]

assert sol.shortestAlternatingPaths(3, [[0, 1], [1, 2]], []) == [0, 1, -1]
assert sol.shortestAlternatingPaths(3, [[0, 1]], [[2, 1]]) == [0, 1, -1]

assert Solution().shortestAlternatingPaths(1, [], []) == [0]
assert Solution().shortestAlternatingPaths(2, [[0, 1]], [[1, 0]]) == [0, 1]
assert Solution().shortestAlternatingPaths(
    3, [[0, 1], [1, 2], [2, 0]], [[0, 2], [2, 1], [1, 0]]
) == [0, 1, 1]
Solution().shortestAlternatingPaths(
    4, [[0, 1], [1, 2], [2, 3]], [[0, 1], [1, 2], [2, 3]]
) == [0, 1, 2, 3]
# assert Solution().shortestAlternatingPaths(
#     5,
#     [[0, 1], [1, 2], [2, 3], [3, 4], [4, 0]],
#     [[0, 1], [1, 2], [2, 3], [3, 4], [4, 0]],
# ) == [0, 1, 2, 3, 4]
# assert Solution().shortestAlternatingPaths(3, [[0, 0], [0, 1]], [[1, 1], [1, 2]]) == [
#     0,
#     1,
#     2,
# ]

assert Solution().shortestAlternatingPaths(3, [[0, 1]], [[1, 2], [2, 1]]) == [0, 1, 2]
assert Solution().shortestAlternatingPaths(
    100, [[i, i + 1] for i in range(99)], [[i + 1, i] for i in range(99)]
) == [
    0,
    1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
]
assert Solution().shortestAlternatingPaths(3, [], []) == [0, -1, -1]
assert Solution().shortestAlternatingPaths(4, [[0, 1], [1, 2], [2, 3]], []) == [
    0,
    1,
    -1,
    -1,
]
assert Solution().shortestAlternatingPaths(4, [], [[0, 1], [1, 2], [2, 3]]) == [
    0,
    1,
    -1,
    -1,
]
