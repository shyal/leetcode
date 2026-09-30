# REFERENCE: d180 Kahn Queue Loop
class Solution:
    def findOrder(self, numCourses, prerequisites):
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
