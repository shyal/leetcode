"""
URL: https://leetcode.com/problems/widest-vertical-area-between-two-points-containing-no-points/description/

1637. Widest Vertical Area Between Two Points Containing No Points

Given an array of 2D points on a plane, return the widest vertical area between two points such that no points are inside the area.

A vertical area is an area of fixed-width extending infinitely along the y-axis (i.e., infinite height). The widest vertical area is the one with the maximum width.

Note that points on the edge of a vertical area are not considered included in the area.


Example 1:

Input: points = [[8,7],[9,9],[7,4],[9,7]]
Output: 1
Explanation: Both the red and the blue areas are optimal.

Example 2:

Input: points = [[3,1],[9,0],[1,0],[1,4],[5,3],[8,8]]
Output: 3


Constraints:

    n == points.length
    2 <= n <= 10^5
    points[i].length == 2
    0 <= xi, yi <= 10^9
"""


class Solution:
    def maxWidthOfVerticalArea(self, points: List[List[int]]) -> int:
        return max(
            b - a for a, b in pairwise(x[0] for x in sorted(points, key=lambda x: x[0]))
        )


sol = Solution()

assert sol.maxWidthOfVerticalArea([[8, 7], [9, 9], [7, 4], [9, 7]]) == 1
assert sol.maxWidthOfVerticalArea([[3, 1], [9, 0], [1, 0], [1, 4], [5, 3], [8, 8]]) == 3
assert sol.maxWidthOfVerticalArea([[0, 0], [1, 0]]) == 1
assert sol.maxWidthOfVerticalArea([[0, 0], [0, 1]]) == 0
assert sol.maxWidthOfVerticalArea([[5, 1], [5, 2], [5, 3]]) == 0
assert sol.maxWidthOfVerticalArea([[1, 0], [3, 0], [5, 0]]) == 2
assert sol.maxWidthOfVerticalArea([[0, 0], [1000000000, 0]]) == 1000000000
assert sol.maxWidthOfVerticalArea([[1, 1], [1, 1], [1, 1]]) == 0
assert sol.maxWidthOfVerticalArea([[10, 5], [1, 2], [3, 4], [7, 6], [10, 8]]) == 4
assert sol.maxWidthOfVerticalArea([[2, 2], [4, 4], [6, 6], [8, 8], [10, 10]]) == 2
assert (
    sol.maxWidthOfVerticalArea([[1, 100], [100, 1], [50, 50], [0, 0], [99, 99]]) == 49
)
assert sol.maxWidthOfVerticalArea([[0, 0], [0, 0]]) == 0
