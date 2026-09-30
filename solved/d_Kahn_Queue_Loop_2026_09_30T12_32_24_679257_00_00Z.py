"""
DRILL: Kahn Queue Loop

The pair [a, b] in prerequisites means course b is a prerequisite of
course a. Return the courses 0 to numCourses - 1 in an order that puts
every course after all of its prerequisites. Return [] when no such
order exists.

The stub builds four things:

    adj[b]   the courses that have b as a prerequisite
    deg[a]   the number of prerequisites of a that are not yet in res
    q        the courses whose count is 0
    res      the courses taken so far, in order

Write the body of the while loop. Take the course at the front of q and
append it to res. Each course in its adj list now waits for one fewer
prerequisite, so lower its count by one. When a count reaches 0, append
that course to q.

For example, with numCourses = 6 and
prerequisites = [[2, 3], [1, 2], [0, 1], [0, 4], [4, 5], [5, 1]]

    3 --> 2 --> 1 --> 5 --> 4 --> 0
                |                 ^
                '-----------------'

we take the courses as so: 3, 2, 1, 5, 4, 0. Course 0 has prerequisites
1 and 4, so its count starts at 2. Taking 1 lowers the count of 0 to 1,
so 0 stays out of q. It also lowers the count of 5 to 0, so 5 joins q.
Taking 4 lowers the count of 0 to 0, and 0 joins q.

A course on a cycle never reaches count 0. It is never taken, res comes
out short, and the stub's last line returns [].

Use Kahn's algorithm.

Example 1:

Input: numCourses = 6, prerequisites = [[2, 3], [1, 2], [0, 1], [0, 4], [4, 5], [5, 1]]
Output: [3, 2, 1, 5, 4, 0]
Explanation: course 0 has prerequisites 1 and 4. It is taken after 4,
which is the later of the two. No other order is correct.

Example 2:

Input: numCourses = 4, prerequisites = [[1, 0], [2, 0], [3, 1], [3, 2]]

    .--> 1 --.
    |        v
    0        3
    |        ^
    '--> 2 --'

Output: [0, 1, 2, 3]
Explanation: [0, 2, 1, 3] is also correct.

Example 3:

Input: numCourses = 4, prerequisites = [[1, 0], [2, 1], [3, 2], [1, 3]]

    0 --> 1 --> 2 --> 3
          ^           |
          '-----------'

Output: []
Explanation: course 0 is taken. Courses 1, 2 and 3 are on a cycle, so
res is [0] and no order exists.

Constraints:

    1 <= numCourses <= 2000
    0 <= len(prerequisites) <= 5000
    All pairs are distinct, and a != b.

    REQUIRED: keep the stub's lines and write only the loop body. It must
    run in O(numCourses + len(prerequisites)) time. NO seen set.
---
Learning
"""


# mu 0.7
# def findOrder(numCourses: int, prerequisites: [[int]]) -> [int]
#   adj = adjacency(prerequisites, numCourses, reverse=true)
#   deg = indegrees(prerequisites, numCourses, reverse=true)
#   q = deque([n for n in deg if deg[n] == 0])
#   res = []
#   while q
#     node = q.popleft()
#     res <- node
#     for nxt in adj[node]
#       deg[nxt] -= 1
#       if deg[nxt] == 0
#         q <- nxt
#   res if len(res) == numCourses else []

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


def table(*dims, fill=0):
    if len(dims) == 1:
        return [fill] * dims[0]
    if len(dims) == 2:
        return [[fill] * dims[1] for _ in range(dims[0])]
    return [table(*dims[1:], fill=fill) for _ in range(dims[0])]


def indegrees(edges, n=None, reverse=False, directed=True, type=defaultdict):
    if type is list:
        if n is None:
            raise ValueError("type=list needs n")
        indeg = table(n)
    else:
        indeg = defaultdict(int)
        for c in range(n or 0):
            indeg[c]
    for e in edges:
        a, b = e[:2]
        if reverse:
            a, b = b, a
        indeg[b] += 1
        if not directed:
            indeg[a] += 1
    return indeg


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
            adj = adjacency(prerequisites, numCourses, reverse=True)
            deg = indegrees(prerequisites, numCourses, reverse=True)
            q = deque([n for n in deg if deg[n] == 0])
            res = []
            while q:
                node = q.popleft()
                res.append(node)
                for nxt in adj[node]:
                    deg[nxt] -= 1
                    if deg[nxt] == 0:
                        q.append(nxt)
            return res if len(res) == numCourses else []
        finally:
            _in_prerequisites[:] = _w_prerequisites


sol = Solution()
print(sol.findOrder(6, [[2, 3], [1, 2], [0, 1], [0, 4], [4, 5], [5, 1]]))
assert sol.findOrder(4, [[1, 0], [2, 0], [3, 1], [3, 2]]) in ([0, 1, 2, 3], [0, 2, 1, 3])
assert sol.findOrder(4, [[1, 0], [2, 1], [3, 2], [3, 0]]) == [0, 1, 2, 3]
assert sol.findOrder(4, [[1, 0], [2, 1], [3, 2], [1, 3]]) == []
assert sol.findOrder(1, []) == [0]
assert sorted(sol.findOrder(3, [])) == [0, 1, 2]
assert sol.findOrder(2, [[1, 0]]) == [0, 1]
assert sol.findOrder(2, [[0, 1]]) == [1, 0]
assert sol.findOrder(2, [[1, 0], [0, 1]]) == []
assert sol.findOrder(3, [[1, 0], [2, 1], [0, 2]]) == []
assert sol.findOrder(4, [[1, 0], [3, 2]]) in ([0, 1, 2, 3], [0, 2, 1, 3], [0, 2, 3, 1], [2, 0, 1, 3], [2, 0, 3, 1], [2, 3, 0, 1])
assert sol.findOrder(3, [[2, 0], [2, 1]]) in ([0, 1, 2], [1, 0, 2])
assert sol.findOrder(6, [[1, 0], [2, 1], [3, 2], [4, 3], [4, 0], [5, 4]]) == [0, 1, 2, 3, 4, 5]
assert sol.findOrder(6, [[2, 3], [1, 2], [0, 1], [0, 4], [4, 5], [5, 1]]) == [3, 2, 1, 5, 4, 0]
assert sol.findOrder(5, [[0, 4], [1, 4], [2, 0], [2, 1], [3, 2]]) in ([4, 0, 1, 2, 3], [4, 1, 0, 2, 3])
assert sol.findOrder(2000, [[i + 1, i] for i in range(0, 1999)]) == list(range(0, 2000))
assert sol.findOrder(2000, [[i, i + 1] for i in range(0, 1999)]) == list(range(1999, -1, -1))
assert sol.findOrder(2000, [[(i + 1) % 2000, i] for i in range(0, 2000)]) == []
