"""
URL: https://leetcode.com/problems/course-schedule/description/?envType=problem-list-v2&envId=vn57k9wr

207. Course Schedule

There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. You are given an array prerequisites where prerequisites[i] = [a_i, b_i] indicates that you must take course b_i first if you want to take course a_i.

For example, the pair [0, 1], indicates that to take course 0 you have to first take course 1.

Return true if you can finish all courses. Otherwise, return false.

Example 1:

Input: numCourses = 2, prerequisites = [[1,0]]
Output: true
Explanation: There are a total of 2 courses to take.
To take course 1 you should have finished course 0. So it is possible.

Example 2:

Input: numCourses = 2, prerequisites = [[1,0],[0,1]]
Output: false
Explanation: There are a total of 2 courses to take.
To take course 1 you should have finished course 0, and to take course 0 you should also have finished course 1. So it is impossible.

Constraints:

    1 <= numCourses <= 2000
    0 <= prerequisites.length <= 5000
    prerequisites[i].length == 2
    0 <= a_i, b_i < numCourses
    All the pairs prerequisites[i] are unique.

---

Apparently this was my solution in 2025.. copied my own solution.

"""


class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        @cache
        def dfs(i, count):
            if count > numCourses:
                return False
            for req in G[i]:
                if not dfs(req, count + 1):
                    return False
            return True

        G = defaultdict(list)

        for x, y in prerequisites:
            G[x].append(y)

        for i in range(numCourses):
            res = dfs(i, 0)
            if not res:
                return False

        return True


sol = Solution()

# print(sol.canFinish(2, [[1, 0]]))  # True
print(sol.canFinish(4, [[1, 0], [2, 0], [3, 1], [3, 2]]))  # True

assert sol.canFinish(2, [[1, 0]]) == True
assert sol.canFinish(2, [[1, 0], [0, 1]]) == False

assert sol.canFinish(1, []) == True
assert sol.canFinish(1, [[0, 0]]) == False
assert sol.canFinish(3, [[1, 0], [2, 1]]) == True
assert sol.canFinish(3, [[1, 0], [2, 1], [0, 2]]) == False
assert sol.canFinish(4, [[1, 0], [2, 0], [3, 1], [3, 2]]) == True
assert sol.canFinish(4, [[1, 0], [2, 0], [3, 1], [3, 2], [0, 3]]) == False
assert sol.canFinish(2000, []) == True
# assert sol.canFinish(2000, [[i + 1, i] for i in range(1999)]) == True
# assert sol.canFinish(2000, [[i, i + 1] for i in range(1999)]) == True
assert sol.canFinish(5, [[1, 0], [2, 0], [3, 1], [4, 3], [1, 4]]) == False
assert sol.canFinish(2, []) == True
assert sol.canFinish(2, [[0, 1], [1, 0]]) == False
