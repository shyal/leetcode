"""
URL: https://leetcode.com/problems/course-schedule-ii/description/?envType=problem-list-v2&envId=vn57k9wr

210. Course Schedule II

There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. You are given an array prerequisites where prerequisites[i] = [a_i, b_i] indicates that you must take course b_i first if you want to take course a_i.

For example, the pair [0, 1], indicates that to take course 0 you have to first take course 1.

    1 --> 0

(an arrow b --> a means take b before a)

Return the ordering of courses you should take to finish all courses. If there are many valid answers, return any of them. If it is impossible to finish all courses, return an empty array.

Example 1:

Input: numCourses = 2, prerequisites = [[1,0]]

    0 --> 1

Output: [0,1]
Explanation: There are a total of 2 courses to take. To take course 1 you should have finished course 0. So the correct course order is [0,1].

Example 2:

Input: numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]

    .--> 1 --.
    |        v
    0        3
    |        ^
    '--> 2 --'

Output: [0,2,1,3]
Explanation: There are a total of 4 courses to take. To take course 3 you should have finished both courses 1 and 2. Both courses 1 and 2 should be taken after you finished course 0.
So one correct course order is [0,1,2,3]. Another correct ordering is [0,2,1,3].

Example 3:

Input: numCourses = 1, prerequisites = []

    0

Output: [0]

Example 4:

Input: numCourses = 6, prerequisites = [[2,0],[2,1],[3,2],[4,2],[5,3],[5,4]]

    0 --.        .--> 3 --.
        v        |        v
        2 -------+        5
        ^        |        ^
    1 --'        '--> 4 --'

Output: [0,1,2,3,4,5]
Explanation: Courses 0 and 1 have no prerequisites. Course 2 needs both. Courses 3 and 4 both need 2, and course 5 needs 3 and 4. [1,0,2,4,3,5] is also correct.

Example 5:

Input: numCourses = 8, prerequisites = [[1,0],[2,1],[3,1],[4,3],[4,0],[6,5]]

    0 ------> 1 ------> 2
    |         |
    |         v
    |         3
    |         |
    v         |
    4 <-------'          5 --> 6          7

Output: [0,5,7,1,6,2,3,4]
Explanation: Course 4 needs 0 and 3, and 3 needs 1, which needs 0. Courses 5 and 6 are a separate chain. Course 7 has no prerequisites and nothing needs it. Any order that respects the arrows is correct.

Constraints:

    1 <= numCourses <= 2000
    0 <= prerequisites.length <= numCourses * (numCourses - 1)
    prerequisites[i].length == 2
    0 <= a_i, b_i < numCourses
    a_i != b_i
    All the pairs [a_i, b_i] are distinct.
---
Got close:

def findOrder(numCourses: int, prerequisites: [[int]]) -> [int]
  deg = {}
  for n in range(numCourses)
    deg[n] = 0
  for (a, b) in prerequisites
    deg[b] += 1
  print(deg)
  adj = adjacency(prerequisites, numCourses)
  print(adj)
  q = deque([n for n in deg if deg[n] == 0])
  print(q)
  res = {:list}
  seen = set()
  for (d, node) in levels(q, seen=seen)
    res[d] <- node
    for nxt in adj[node]
      q.append(nxt)
  print_orig(res)
  [*chain.from_iterable([res[k] for k in sorted(res, reverse=True)])]

sol = Solution()
passed all the test cases that were given.. however not this case:
print(sol.findOrder(6, [[2,3],[1,2],[0,1],[0,4],[4,5],[5,1]]))
because i wrote a standard bfs, not a topological sort
Learning

LEETCODE: Accepted (3 ms, 20.6 MB)
"""


# mu 0.7
# def findOrder(numCourses: int, prerequisites: [[int]]) -> [int]
#   deg = {}
#   for n in range(numCourses)
#     deg[n] = 0
#   for (a, b) in prerequisites
#     deg[b] += 1
#   adj = adjacency(prerequisites, numCourses)
#   q = deque([n for n in deg if deg[n] == 0])
#   res = []
#   while q
#     node = q.popleft()
#     res <- node
#     for nxt in adj[node]
#       deg[nxt] -= 1
#       if deg[nxt] == 0
#         q <- nxt
#   res[::-1] if len res == numCourses else []

from collections import defaultdict


def adjacency(edges, n=None, reverse=False, directed=True, weighted=False):
    adj = defaultdict(dict) if weighted else defaultdict(list)
    for c in range(n or 0):
        adj[c]
    for e in edges:
        a, b = e[:2]
        if reverse:
            a, b = b, a
        if weighted:
            adj[a][b] = e[2]
            if not directed:
                adj[b][a] = e[2]
        else:
            adj[a].append(b)
            if not directed:
                adj[b].append(a)
    return adj


class Grid(list):
    """A list of rows that also takes a (row, col) pair as an index."""

    def __getitem__(self, k):
        if type(k) is tuple:
            return list.__getitem__(self, k[0])[k[1]]
        return list.__getitem__(self, k)

    def __setitem__(self, k, v):
        if type(k) is tuple:
            list.__getitem__(self, k[0])[k[1]] = v
        else:
            list.__setitem__(self, k, v)


class Solution:
    def findOrder(self, numCourses: int, prerequisites: list[list[int]]) -> list[int]:
        _in_prerequisites, prerequisites = prerequisites, Grid(prerequisites)
        _w_prerequisites = prerequisites
        try:
            deg = {}
            for n in range(numCourses):
                deg[n] = 0
            for (a, b) in prerequisites:
                deg[b] += 1
            adj = adjacency(prerequisites, numCourses)
            q = deque([n for n in deg if deg[n] == 0])
            res = []
            while q:
                node = q.popleft()
                res.append(node)
                for nxt in adj[node]:
                    deg[nxt] -= 1
                    if deg[nxt] == 0:
                        q.append(nxt)
            return res[::-1] if len(res) == numCourses else []
        finally:
            _in_prerequisites[:] = _w_prerequisites


sol = Solution()
assert sol.findOrder(6, [[2, 3], [1, 2], [0, 1], [0, 4], [4, 5], [5, 1]]) == [3, 2, 1, 5, 4, 0]
assert sol.findOrder(2, [[1, 0]]) == [0, 1]
assert sol.findOrder(4, [[1, 0], [2, 0], [3, 1], [3, 2]]) in ([0, 1, 2, 3], [0, 2, 1, 3])
assert sol.findOrder(1, []) == [0]
assert Solution().findOrder(0, []) == []
assert Solution().findOrder(1, []) == [0]
assert Solution().findOrder(3, [[1, 0], [2, 0]]) in ([0, 1, 2], [0, 2, 1])
assert Solution().findOrder(3, [[1, 0], [2, 1], [0, 2]]) == []
assert Solution().findOrder(5, [[1, 0], [2, 1], [3, 2], [4, 3]]) == [0, 1, 2, 3, 4]
assert Solution().findOrder(5, [[1, 0], [2, 0], [3, 1], [4, 1], [4, 2]]) in ([0, 1, 2, 3, 4], [0, 1, 2, 4, 3], [0, 1, 3, 2, 4], [0, 2, 1, 3, 4], [0, 2, 1, 4, 3])
assert Solution().findOrder(2, [[1, 0], [0, 1]]) == []
assert Solution().findOrder(3, [[1, 0], [1, 0], [2, 1]]) == [0, 1, 2]
assert Solution().findOrder(4, [[1, 0], [2, 0], [3, 1], [3, 2], [1, 3]]) == []
assert Solution().findOrder(4, [[1, 0], [2, 0], [3, 1], [3, 2]]) in ([0, 1, 2, 3], [0, 2, 1, 3])
assert Solution().findOrder(2, []) in ([0, 1], [1, 0])
