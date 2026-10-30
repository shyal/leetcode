# URL: https://leetcode.com/problems/course-schedule-ii/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 210. Course Schedule II
#
# There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. You are given an array prerequisites where prerequisites[i] = [a_i, b_i] indicates that you must take course b_i first if you want to take course a_i.
#
# For example, the pair [0, 1], indicates that to take course 0 you have to first take course 1.
#
#     1 --> 0
#
# (an arrow b --> a means take b before a)
#
# Return the ordering of courses you should take to finish all courses. If there are many valid answers, return any of them. If it is impossible to finish all courses, return an empty array.
#
# Example 1:
#
# Input: numCourses = 2, prerequisites = [[1,0]]
#
#     0 --> 1
#
# Output: [0,1]
# Explanation: There are a total of 2 courses to take. To take course 1 you should have finished course 0. So the correct course order is [0,1].
#
# Example 2:
#
# Input: numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]
#
#     .--> 1 --.
#     |        v
#     0        3
#     |        ^
#     '--> 2 --'
#
# Output: [0,2,1,3]
# Explanation: There are a total of 4 courses to take. To take course 3 you should have finished both courses 1 and 2. Both courses 1 and 2 should be taken after you finished course 0.
# So one correct course order is [0,1,2,3]. Another correct ordering is [0,2,1,3].
#
# Example 3:
#
# Input: numCourses = 1, prerequisites = []
#
#     0
#
# Output: [0]
#
# Example 4:
#
# Input: numCourses = 6, prerequisites = [[2,0],[2,1],[3,2],[4,2],[5,3],[5,4]]
#
#     0 --.        .--> 3 --.
#         v        |        v
#         2 -------+        5
#         ^        |        ^
#     1 --'        '--> 4 --'
#
# Output: [0,1,2,3,4,5]
# Explanation: Courses 0 and 1 have no prerequisites. Course 2 needs both. Courses 3 and 4 both need 2, and course 5 needs 3 and 4. [1,0,2,4,3,5] is also correct.
#
# Example 5:
#
# Input: numCourses = 8, prerequisites = [[1,0],[2,1],[3,1],[4,3],[4,0],[6,5]]
#
#     0 ------> 1 ------> 2
#     |         |
#     |         v
#     |         3
#     |         |
#     v         |
#     4 <-------'          5 --> 6          7
#
# Output: [0,5,7,1,6,2,3,4]
# Explanation: Course 4 needs 0 and 3, and 3 needs 1, which needs 0. Courses 5 and 6 are a separate chain. Course 7 has no prerequisites and nothing needs it. Any order that respects the arrows is correct.
#
# Constraints:
#
#     1 <= numCourses <= 2000
#     0 <= prerequisites.length <= numCourses * (numCourses - 1)
#     prerequisites[i].length == 2
#     0 <= a_i, b_i < numCourses
#     a_i != b_i
#     All the pairs [a_i, b_i] are distinct.
#
# ---
# LEETCODE: Accepted (7 ms, 20.7 MB)

# mu 0.14

class Solution
  def findOrder(numCourses: int, prerequisites: [[int]]) -> [int]
    G = adjacency(prerequisites, numCourses, true, true)
    in_deg = indegrees(prerequisites, numCourses, true)
    seen = set([])
    # print(G)
    # print(in_deg)
    res = []
    q = deque([x for x in 0..numCourses-1 if in_deg[x] == 0])
    while q
      course = q.popleft()
      if course in seen
        continue
      seen.add(course)
      res <- course
      for next in G[course]
        in_deg[next] -= 1
        if in_deg[next] == 0
          q <- next
    # res or [] if len(res) != numCourses

    if len(res) == numCourses
      return res
    []

      

sol = Solution()

print(sol.findOrder(2, [[1, 0]]))  # [0,1]

assert uses(Solution, adjacency, indegrees)
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
assert Solution().findOrder(6, [[2, 3], [1, 2], [0, 1], [0, 4], [4, 5], [5, 1]]) == [3, 2, 1, 5, 4, 0]
