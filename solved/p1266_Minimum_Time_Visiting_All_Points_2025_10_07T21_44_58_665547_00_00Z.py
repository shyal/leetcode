"""
URL: https://leetcode.com/problems/minimum-time-visiting-all-points/description/?envType=problem-list-v2&envId=geometry

1266. Minimum Time Visiting All Points

On a 2D plane, there are n points with integer coordinates points[i] = [xi, yi]. You are initially positioned at point (x1, y1), which is points[0].

You visit the points in the order given by the array points. To move from a point (x1, y1) to a point (x2, y2), the time taken is max(|x2 - x1|, |y2 - y1|).

Return the minimum time in seconds to visit all the points in the order given by points.


Example 1:

Input: points = [[1,1],[3,4],[-1,0]]
Output: 7
Explanation: One optimal path is [1,1] -> [3,4] -> [-1,0]
Time from [1,1] to [3,4] = 3
Time from [3,4] to [-1,0] = 4
Total time = 7

Example 2:

Input: points = [[3,2],[-2,2]]
Output: 5


Constraints:

    points.length == n
    1 <= n <= 100
    points[i].length == 2
    -1000 <= xi, yi <= 1000

"""


class Solution:
    def minTimeToVisitAllPoints(self, points: List[List[int]]) -> int:
        return reduce(
            lambda acc, P: acc + max(abs(P[1][0] - P[0][0]), abs(P[1][1] - P[0][1])),
            pairwise(points),
            0,
        )


sol = Solution()

# print(sol.minTimeToVisitAllPoints([[1, 1], [3, 4], [-1, 0]]))  # 7

assert sol.minTimeToVisitAllPoints([[1, 1], [3, 4], [-1, 0]]) == 7
assert sol.minTimeToVisitAllPoints([[3, 2], [-2, 2]]) == 5
assert sol.minTimeToVisitAllPoints([[0, 0]]) == 0
assert sol.minTimeToVisitAllPoints([[1, 1], [1, 1]]) == 0
assert sol.minTimeToVisitAllPoints([[0, 0], [5, 0]]) == 5
assert sol.minTimeToVisitAllPoints([[0, 0], [0, 5]]) == 5
assert sol.minTimeToVisitAllPoints([[0, 0], [3, 3]]) == 3
assert sol.minTimeToVisitAllPoints([[0, 0], [3, 5]]) == 5
assert sol.minTimeToVisitAllPoints([[-1000, -1000], [1000, 1000]]) == 2000
assert sol.minTimeToVisitAllPoints([[1, 1], [1, 1], [1, 1]]) == 0
assert sol.minTimeToVisitAllPoints([[1, 1], [3, 4], [-1, 0], [0, 0]]) == 8
assert sol.minTimeToVisitAllPoints([[0, 0], [1, 0], [0, 0]]) == 2
assert sol.minTimeToVisitAllPoints([[5, 5]]) == 0
assert sol.minTimeToVisitAllPoints([[-5, -5], [5, 5]]) == 10
