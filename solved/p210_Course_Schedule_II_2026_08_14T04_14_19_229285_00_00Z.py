"""
URL: https://leetcode.com/problems/course-schedule-ii/description/?envType=problem-list-v2&envId=vn57k9wr

210. Course Schedule II

There are a total of numCourses courses you have to take, labeled from 0 to
numCourses - 1. You are given an array prerequisites where
prerequisites[i] = [ai, bi] indicates that you must take course bi first if
you want to take course ai.

    - For example, the pair [0, 1], indicates that to take course 0 you have
      to first take course 1.

Return the ordering of courses you should take to finish all courses. If
there are many valid answers, return any of them. If it is impossible to
finish all courses, return an empty array.


Example 1:

Input: numCourses = 2, prerequisites = [[1,0]]
Output: [0,1]
Explanation: There are a total of 2 courses to take. To take course 1 you
should have finished course 0. So the correct course order is [0,1].

Example 2:

Input: numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]
Output: [0,2,1,3]
Explanation: There are a total of 4 courses to take. To take course 3 you
should have finished both courses 1 and 2. Both courses 1 and 2 should be
taken after you finished course 0.
So one correct course order is [0,1,2,3]. Another correct ordering is
[0,2,1,3].

Example 3:

Input: numCourses = 1, prerequisites = []
Output: [0]


Constraints:

    1 <= numCourses <= 2000
    0 <= prerequisites.length <= numCourses * (numCourses - 1)
    prerequisites[i].length == 2
    0 <= ai, bi < numCourses
    ai != bi
    All the pairs [ai, bi] are distinct.

---

This completely slipped my mind, so i got heavily hinted with pseudocode:

1. Count, for each course, how many prerequisites point into it (its indegree).
2. Start a queue with every course whose indegree is 0 — those you can take right now.
3. Pop a course, append it to your order, then "remove" it: for each course that depended on it, drop that indegree by 1. Any that hit 0 join the queue.
4. When the queue empties: if your order has all numCourses entries, that's the answer. If it's shorter, there was a cycle — return [].

Then i got a couple of things wrong (checking the wrong variable, and a small issue with the append logic).

"""


class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        indegree = {x: 0 for x in range(numCourses)}
        for course, _ in prerequisites:
            indegree[course] += 1
        d = deque([x for x in range(numCourses) if indegree[x] == 0])
        order = []
        while d:
            cur = d.popleft()
            order.append(cur)
            dependents = [course for course, req in prerequisites if req == cur]
            for course in dependents:
                indegree[course] -= 1
                if indegree[course] == 0:
                    d.append(course)
        if len(order) == numCourses:
            return order
        return []


sol = Solution()

# print(sol.findOrder(2, [[1, 0]]))  # [0, 1]

assert sol.findOrder(2, [[1, 0]]) == [0, 1]
assert sol.findOrder(4, [[1, 0], [2, 0], [3, 1], [3, 2]]) == [0, 1, 2, 3]
assert sol.findOrder(1, []) == [0]
assert sol.findOrder(2, [[0, 1], [1, 0]]) == []
assert sol.findOrder(3, [[1, 0], [2, 1], [0, 2]]) == []
assert sol.findOrder(2, []) == [0, 1]
assert sol.findOrder(3, []) == [0, 1, 2]
assert sol.findOrder(4, [[1, 2], [2, 1]]) == []
assert sol.findOrder(5, [[1, 0], [2, 1], [3, 2], [4, 3]]) == [0, 1, 2, 3, 4]
assert sol.findOrder(3, [[0, 1], [1, 2]]) == [2, 1, 0]
assert sol.findOrder(3, [[2, 0], [2, 1]]) == [0, 1, 2]
assert sol.findOrder(6, [[5, 0], [5, 2], [4, 0], [4, 1], [2, 3], [3, 1]]) == [0, 1, 4, 3, 2, 5]
assert sol.findOrder(5, [[1, 0], [2, 1], [1, 2], [4, 3]]) == []