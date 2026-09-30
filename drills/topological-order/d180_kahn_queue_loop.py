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
"""


class Solution:

    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        adj = adjacency(prerequisites, numCourses, reverse=True)
        deg = indegrees(prerequisites, numCourses, reverse=True)
        q = deque([n for n in deg if deg[n] == 0])
        res = []
        while q:
            pass
        return res if len(res) == numCourses else []


sol = Solution()

print(sol.findOrder(6, [[2, 3], [1, 2], [0, 1], [0, 4], [4, 5], [5, 1]]))  # [3, 2, 1, 5, 4, 0]

# assert sol.findOrder(4, [[1, 0], [2, 0], [3, 1], [3, 2]]) in (
#     [0, 1, 2, 3],
#     [0, 2, 1, 3],
# )
# assert sol.findOrder(4, [[1, 0], [2, 1], [3, 2], [3, 0]]) == [0, 1, 2, 3]
# assert sol.findOrder(4, [[1, 0], [2, 1], [3, 2], [1, 3]]) == []
# assert sol.findOrder(1, []) == [0]
# assert sorted(sol.findOrder(3, [])) == [0, 1, 2]
# assert sol.findOrder(2, [[1, 0]]) == [0, 1]
# assert sol.findOrder(2, [[0, 1]]) == [1, 0]
# assert sol.findOrder(2, [[1, 0], [0, 1]]) == []
# assert sol.findOrder(3, [[1, 0], [2, 1], [0, 2]]) == []
# assert sol.findOrder(4, [[1, 0], [3, 2]]) in (
#     [0, 1, 2, 3],
#     [0, 2, 1, 3],
#     [0, 2, 3, 1],
#     [2, 0, 1, 3],
#     [2, 0, 3, 1],
#     [2, 3, 0, 1],
# )
# assert sol.findOrder(3, [[2, 0], [2, 1]]) in (
#     [0, 1, 2],
#     [1, 0, 2],
# )
# assert sol.findOrder(6, [[1, 0], [2, 1], [3, 2], [4, 3], [4, 0], [5, 4]]) == [0, 1, 2, 3, 4, 5]
# assert sol.findOrder(6, [[2, 3], [1, 2], [0, 1], [0, 4], [4, 5], [5, 1]]) == [3, 2, 1, 5, 4, 0]
# assert sol.findOrder(5, [[0, 4], [1, 4], [2, 0], [2, 1], [3, 2]]) in (
#     [4, 0, 1, 2, 3],
#     [4, 1, 0, 2, 3],
# )
# assert sol.findOrder(2000, [[i + 1, i] for i in range(1999)]) == list(range(2000))
# assert sol.findOrder(2000, [[i, i + 1] for i in range(1999)]) == list(range(1999, -1, -1))
# assert sol.findOrder(2000, [[(i + 1) % 2000, i] for i in range(2000)]) == []
