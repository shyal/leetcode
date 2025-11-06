"""
URL: https://leetcode.com/problems/min-cost-to-connect-all-points/description/?envType=problem-list-v2&envId=vn57k9wr

1584. Min Cost to Connect All Points

You are given an array points representing integer coordinates of some points on a 2D-plane, where points[i] = [x_i, y_i].

The cost of connecting two points [x_i, y_i] and [x_j, y_j] is the manhattan distance between them: |x_i - x_j| + |y_i - y_j|, where |val| denotes the absolute value of val.

Return the minimum cost to make all points connected. All points are connected if there is exactly one simple path between any two points.


Example 1:

Input: points = [[0,0],[2,2],[3,10],[5,2],[7,0]]
Output: 20
Explanation:
We can connect the points as shown above to get the minimum cost of 20.
Notice that there is a unique path between every pair of points.

Example 2:

Input: points = [[3,12],[-2,5],[-4,1]]
Output: 18


Constraints:

    1 <= points.length <= 1000
    -10^6 <= x_i, y_i <= 10^6
    All pairs (x_i, y_i) are distinct.
"""


class Solution:
    def minCostConnectPoints(self, p: List[List[int]]) -> int:
        edges = sorted(
            [
                (abs(p[i][0] - p[j][0]) + abs(p[i][1] - p[j][1]), i, j)
                for i, j in combinations(range(len(p)), 2)
            ]
        )

        parent = list(range(len(p)))

        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def union(x, y):
            px, py = find(x), find(y)
            if px == py:
                return False
            parent[py] = px
            return True

        total_cost = 0
        edges_used = 0
        for dist, u, v in edges:
            if union(u, v):
                total_cost += dist
                edges_used += 1
                if edges_used == len(p) - 1:
                    break

        return total_cost


sol = Solution()

# print(sol.minCostConnectPoints([[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]))  # 20

assert sol.minCostConnectPoints([[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]) == 20
assert sol.minCostConnectPoints([[3, 12], [-2, 5], [-4, 1]]) == 18
assert sol.minCostConnectPoints([]) == 0
assert sol.minCostConnectPoints([[5, 5]]) == 0
assert sol.minCostConnectPoints([[0, 0], [1, 1]]) == 2
assert sol.minCostConnectPoints([[0, 0], [0, 1], [0, 2]]) == 2
assert sol.minCostConnectPoints([[1, 1], [2, 2], [3, 3], [4, 4]]) == 6
assert sol.minCostConnectPoints([[0, 0], [3, 0], [0, 4]]) == 7
assert (
    sol.minCostConnectPoints([[-1000000, -1000000], [1000000, 1000000]]) == 4000000
)  # assert sol.minCostConnectPoints([[-1000000,-1000000],[1000000,1000000]]) == 4000000
