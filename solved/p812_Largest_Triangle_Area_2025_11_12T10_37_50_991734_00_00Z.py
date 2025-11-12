"""
URL: https://leetcode.com/problems/largest-triangle-area/description/?envType=problem-list-v2&envId=vn57k9wr

812. Largest Triangle Area

Given an array of points on the X-Y plane points where points[i] = [x_i, y_i], return the area of the largest triangle that can be formed by any three different points. Answers within 10^-5 of the actual answer will be accepted.

Example 1:

Input: points = [[0,0],[0,1],[1,0],[0,2],[2,0]]
Output: 2.00000
Explanation: The five points are shown in the above figure. The red triangle is the largest.

Example 2:

Input: points = [[1,0],[0,0],[0,1]]
Output: 0.50000

Constraints:

    3 <= points.length <= 50
    -50 <= x_i, y_i <= 50
    All the given points are unique.

---

Not sure i'd be able to summon up the shoelace formula in an interview setting.

"""


class Solution:

    def getArea(self, a, b, c):
        x1, y1 = a
        x2, y2 = b
        x3, y3 = c
        Area = abs(0.5 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)))
        return round(Area, ndigits=5)

    def largestTriangleArea(self, points: List[List[int]]) -> float:
        _max = 0
        for i, j, k in combinations(range(len(points)), 3):
            # print(i, j, k)
            area = self.getArea(points[i], points[j], points[k])
            _max = max(_max, area)
        return _max


sol = Solution()
assert abs(sol.largestTriangleArea([[1, 0], [0, 0], [0, 1]]) - 0.5) < 1e-05
assert abs(sol.largestTriangleArea([[0, 0], [1, 0], [2, 0]]) - 0.0) < 1e-05
assert abs(sol.largestTriangleArea([[0, 0], [1, 0], [2, 0], [3, 0]]) - 0.0) < 1e-05
assert abs(sol.largestTriangleArea([[-1, -1], [1, -1], [0, 1]]) - 2.0) < 1e-05
assert abs(sol.largestTriangleArea([[0, 0], [0, 1], [0, 2]]) - 0.0) < 1e-05
assert abs(sol.largestTriangleArea([[1, 1], [2, 2], [3, 4]]) - 0.5) < 1e-05
assert abs(sol.largestTriangleArea([[0, 0], [3, 0], [0, 4]]) - 6.0) < 1e-05
assert abs(sol.largestTriangleArea([[0, 0], [0, 1], [1, 0], [1, 1]]) - 0.5) < 1e-05
assert abs(sol.largestTriangleArea([[-50, -50], [50, 50], [0, 0]]) - 0.0) < 1e-05
assert abs(sol.largestTriangleArea([[-1, 0], [0, 1], [1, 0]]) - 1.0) < 1e-05
