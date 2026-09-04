"""
URL: https://leetcode.com/problems/widest-vertical-area-between-two-points-containing-no-points/description/?envType=problem-list-v2&envId=vn57k9wr

1637. Widest Vertical Area Between Two Points Containing No Points

Given n points on a 2D plane where points[i] = [x_i, y_i], return the widest vertical area between two points such that no points are inside the area.

A vertical area is an area of fixed-width extending infinitely along the y-axis (i.e., infinite height). The widest vertical area is the one with the maximum width.

Note that points on the edge of a vertical area are not considered included in the area.

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
    0 <= x_i, y_i <= 10^9
"""


class Solution:
    def maxWidthOfVerticalArea(self, points: List[List[int]]) -> int:
        x = [*sorted(set([x[0] for x in points]), reverse=True)]
        if len(x) == 1:
            return 0
        return max(a - b for a, b in zip(x, x[1:]))


sol = Solution()

print(sol.maxWidthOfVerticalArea([[8, 7], [9, 9], [7, 4], [9, 7]]))  # 1

assert sol.maxWidthOfVerticalArea([[8, 7], [9, 9], [7, 4], [9, 7]]) == 1
assert sol.maxWidthOfVerticalArea([[3, 1], [9, 0], [1, 0], [1, 4], [5, 3], [8, 8]]) == 3

assert sol.maxWidthOfVerticalArea([[0, 0], [0, 1]]) == 0
assert sol.maxWidthOfVerticalArea([[1, 1], [1, 1], [1, 1]]) == 0
assert sol.maxWidthOfVerticalArea([[0, 0], [1000000000, 0]]) == 1000000000
assert sol.maxWidthOfVerticalArea([[1, 2], [2, 3], [3, 4], [4, 5], [5, 6]]) == 1
assert sol.maxWidthOfVerticalArea([[1, 1], [1, 2], [1, 3], [10, 1]]) == 9
assert sol.maxWidthOfVerticalArea([[5, 5], [5, 5], [10, 10], [10, 10]]) == 5
assert (
    sol.maxWidthOfVerticalArea([[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [100, 0]])
    == 100
)
assert sol.maxWidthOfVerticalArea([[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0]]) == 1
assert (
    sol.maxWidthOfVerticalArea([[0, 0], [0, 0], [0, 0], [1000000000, 0]]) == 1000000000
)
assert sol.maxWidthOfVerticalArea([[1, 1], [2, 2]]) == 1
assert sol.maxWidthOfVerticalArea([[1, 1], [1000000000, 1000000000]]) == 999999999
assert (
    sol.maxWidthOfVerticalArea(
        [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
    )
    == 0
)
