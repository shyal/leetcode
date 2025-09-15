from typing import List

"""
1037 - Valid Boomerang

Given an array points where points[i] = [xi, yi] represents a point on the X-Y plane, return true if these points are a boomerang.
A boomerang is a set of three points that are all distinct and not in a straight line.

Example 1:

Input: points = [[1,1],[2,3],[3,2]]
Output: true
Example 2:

Input: points = [[1,1],[2,2],[3,3]]
Output: false


Constraints:

points.length == 3
points[i].length == 2
0 <= xi, yi <= 100


# Notes:

This isn't the slop, it's the inverse. 

Todo: Revisit with cross multiplication.

"""


class Solution:
    def isBoomerang(self, points: List[List[int]]) -> bool:
        non_overlapping = all(a != b for a, b in zip(points, points[1:]))

        def get_slope(a, b):
            if a[0] == b[0]:
                return float("-inf")
            elif a[1] == b[1]:
                return float("inf")
            else:
                return (a[0] - b[0]) / (a[1] - b[1])

        slopes = [get_slope(a, b) for a, b in zip(points, points[1:])]

        print(slopes)

        return non_overlapping and slopes[0] != slopes[1]


sol = Solution()
assert sol.isBoomerang([[1, 1], [2, 3], [3, 2]]) == True
assert sol.isBoomerang([[1, 1], [2, 2], [3, 3]]) == False
assert sol.isBoomerang([[0, 1], [0, 2], [1, 2]]) == True
assert sol.isBoomerang([[0, 2], [2, 1], [0, 0]]) == True
assert sol.isBoomerang([[0, 0], [0, 0], [1, 1]]) == False
assert sol.isBoomerang([[0, 0], [0, 0], [0, 0]]) == False
assert sol.isBoomerang([[0, 0], [1, 0], [0, 0]]) == False
assert sol.isBoomerang([[0, 0], [0, 1], [0, 2]]) == False
assert sol.isBoomerang([[0, 0], [1, 0], [2, 0]]) == False
assert sol.isBoomerang([[0, 0], [1, 1], [2, 2]]) == False
assert sol.isBoomerang([[1, 2], [3, 4], [5, 6]]) == False
assert sol.isBoomerang([[-1, 0], [0, 0], [1, 0]]) == False
assert sol.isBoomerang([[0, 0], [1, 1], [2, 3]]) == True
assert sol.isBoomerang([[0, 0], [0, 1], [1, 0]]) == True
assert sol.isBoomerang([[1, 1], [2, 2], [3, 4]]) == True
assert sol.isBoomerang([[-1, -1], [0, 0], [1, 2]]) == True
assert sol.isBoomerang([[100, 100], [200, 200], [300, 301]]) == True
assert sol.isBoomerang([[0, 1], [1, 0], [2, 0]]) == True
assert sol.isBoomerang([[1, 0], [1, 1], [1, 2]]) == False
assert sol.isBoomerang([[2, 2], [3, 3], [1, 1]]) == False
