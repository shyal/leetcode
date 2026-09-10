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

Failed at BFS, and anyway should be using topological sort.

"""


class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        adj = defaultdict(list)
        starts = set(range(numCourses))
        for n in range(numCourses):
            adj[n]
        for a, b in prerequisites:
            adj[b].append(a)
            if a in starts:
                starts.remove(a)

        draw_ascii_graph(adj)

        def bfs(start):
            q = deque([[start, 0]])
            res = defaultdict(list)
            count = 0
            while q:
                count += 1
                if count > len(prerequisites) * 2:
                    return []
                course, dist = q.popleft()
                if course in visited:
                    continue
                visited.add(course)
                res[dist].append(course)
                for dep in adj[course]:
                    q.append([dep, dist + 1])
            return res

        visited = set([])

        print(starts)

        res = []
        for s in starts:
            r = bfs(s)
            for t in sorted(r):
                res.extend(r[t])
        return res


sol = Solution()

# sol.findOrder(
#     numCourses=8, prerequisites=[[1, 0], [2, 1], [3, 1], [4, 3], [4, 0], [6, 5]]
# )

print(sol.findOrder(6, [[2, 0], [2, 1], [3, 2], [4, 2], [5, 3], [5, 4]]))


# print(sol.findOrder(2, [[1, 0]]))  # [0,1]

# assert sol.findOrder(2, [[1, 0]]) == [0, 1]
# assert sol.findOrder(4, [[1, 0], [2, 0], [3, 1], [3, 2]]) in (
#     [0, 1, 2, 3],
#     [0, 2, 1, 3],
# )
# assert sol.findOrder(1, []) == [0]
# # assert sol.findOrder(6, [[2, 0], [2, 1], [3, 2], [4, 2], [5, 3], [5, 4]])[-1] == 5
# assert len(sol.findOrder(8, [[1, 0], [2, 1], [3, 1], [4, 3], [4, 0], [6, 5]])) == 8

# assert Solution().findOrder(0, []) == []
# assert Solution().findOrder(1, []) == [0]
# assert Solution().findOrder(3, [[1, 0], [2, 0]]) == [0, 1, 2]
# assert Solution().findOrder(3, [[1, 0], [2, 1], [0, 2]]) == []
# assert Solution().findOrder(5, [[1, 0], [2, 1], [3, 2], [4, 3]]) == [0, 1, 2, 3, 4]
# assert Solution().findOrder(5, [[1, 0], [2, 0], [3, 1], [4, 1], [4, 2]]) == [
#     0,
#     1,
#     2,
#     3,
#     4,
# ]
# assert Solution().findOrder(2, [[1, 0], [0, 1]]) == []
# assert Solution().findOrder(3, [[1, 0], [1, 0], [2, 1]]) == [0, 1, 2]
# # assert Solution().findOrder(4, [[1, 0], [2, 0], [3, 1], [3, 2], [1, 3]]) == []
# assert Solution().findOrder(4, [[1, 0], [2, 0], [3, 1], [3, 2]]) == [0, 1, 2, 3]
# assert Solution().findOrder(2, []) == [0, 1]


# FAILED: walked away after 41m 1s; no working solution.
# Judge the moves actually attempted as struggled, not clean.
