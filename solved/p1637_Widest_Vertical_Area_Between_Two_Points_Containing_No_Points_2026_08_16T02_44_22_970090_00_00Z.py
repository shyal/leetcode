"""
URL: https://leetcode.com/problems/widest-vertical-area-between-two-points-containing-no-points/description/?envType=problem-list-v2&envId=vn57k9wr

1637. Widest Vertical Area Between Two Points Containing No Points

Given n points on a 2D plane where points[i] = [xi, yi], return the widest
vertical area between two points such that no points are inside the area.

A vertical area is an area of fixed-width extending infinitely along the
y-axis (i.e., infinite height). The widest vertical area is the one with
the maximum width.

Note that points on the edge of a vertical area are not considered
included in the area.


Example 1:

Input: points = [[8,7],[9,9],[7,4],[9,7]]
Output: 1
Explanation: Both the red and the blue area are optimal.

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
        p = sorted([*set(x for x, _ in points)])
        return max(abs(a - b) for a, b in zip(p, p[1:])) if len(p) > 1 else 0


sol = Solution()

# print(sol.maxWidthOfVerticalArea([[8, 7], [9, 9], [7, 4], [9, 7]]))  # 1

assert sol.maxWidthOfVerticalArea([[8, 7], [9, 9], [7, 4], [9, 7]]) == 1
assert sol.maxWidthOfVerticalArea([[3, 1], [9, 0], [1, 0], [1, 4], [5, 3], [8, 8]]) == 3
assert sol.maxWidthOfVerticalArea([[0, 0], [1000000000, 1]]) == 1000000000
assert sol.maxWidthOfVerticalArea([[1000000000, 0], [0, 1000000000]]) == 1000000000
assert sol.maxWidthOfVerticalArea([[5, 5], [5, 9]]) == 0
assert sol.maxWidthOfVerticalArea([[0, 0], [0, 1], [0, 2]]) == 0
assert sol.maxWidthOfVerticalArea([[1, 1], [2, 2], [3, 3]]) == 1
assert sol.maxWidthOfVerticalArea([[10, 0], [1, 0], [7, 0]]) == 6
assert sol.maxWidthOfVerticalArea([[2, 0], [2, 5], [9, 3], [4, 1]]) == 5
assert sol.maxWidthOfVerticalArea([[6, 1], [3, 2], [8, 3], [1, 4]]) == 3
assert sol.maxWidthOfVerticalArea([[9, 0], [8, 1], [7, 2], [6, 3], [0, 4]]) == 6
assert sol.maxWidthOfVerticalArea([[0, 0], [1, 0], [1, 5], [4, 9], [4, 2]]) == 3
assert sol.maxWidthOfVerticalArea([[0, 1000000000], [500000000, 0], [1000000000, 5]]) == 500000000