"""
URL: https://leetcode.com/problems/brick-wall/description/?envType=problem-list-v2&envId=vn57k9wr

554. Brick Wall

There is a rectangular brick wall in front of you with n rows of bricks. The ith row has some number of bricks each of the same height (i.e., one unit) but they can be of different widths. The total width of each row is the same.

Draw a vertical line from the top to the bottom and cross the least bricks. If your line goes through the edge of a brick, then the brick is not considered as crossed. You cannot draw a line just along one of the two vertical edges of the wall, in which case the line will obviously cross no bricks.

Given the 2D array wall that contains the information about the wall, return the minimum number of crossed bricks after drawing such a vertical line.

Example 1:

Input: wall = [[1,2,2,1],[3,1,2],[1,3,2],[2,4],[3,1,2],[1,3,1,1]]
Output: 2

Example 2:

Input: wall = [[1],[1],[1]]
Output: 3

Constraints:

    n == wall.length
    1 <= n <= 10^4
    1 <= wall[i].length <= 10^4
    1 <= sum(wall[i].length) <= 2 * 10^4
    sum(wall[i]) is the same for each row i.
    1 <= wall[i][j] <= 2^31 - 1
---
hinted, also this question is questionable

LEETCODE: Accepted (8 ms, 23 MB)
"""


# mu 0.10
# class Solution
#   def leastBricks(wall: [[int]]) -> int
#     count = {:int}
#     for row in wall
#       c = 0
#       for b in row[:-1]
#         c += b
#         count[c] += 1
#     len(wall) - max(count.values(), default=0)

from collections import defaultdict


class Grid(list):
    """A list of rows that also takes a (row, col) pair as an index."""

    def __getitem__(self, k):
        if type(k) is tuple:
            return list.__getitem__(self, k[0])[k[1]]
        return list.__getitem__(self, k)

    def __setitem__(self, k, v):
        if type(k) is tuple:
            list.__getitem__(self, k[0])[k[1]] = v
        else:
            list.__setitem__(self, k, v)


class Solution:
    def leastBricks(self, wall: list[list[int]]) -> int:
        _in_wall, wall = wall, Grid(wall)
        _w_wall = wall
        try:
            count = defaultdict(int)
            for row in wall:
                c = 0
                for b in row[:-1]:
                    c += b
                    count[c] += 1
            return len(wall) - max(count.values(), default=0)
        finally:
            _in_wall[:] = _w_wall


sol = Solution()
print(sol.leastBricks([[1, 2, 2, 1], [3, 1, 2], [1, 3, 2], [2, 4], [3, 1, 2], [1, 3, 1, 1]]))
_l, _r = sol.leastBricks([[1, 2, 2, 1], [3, 1, 2], [1, 3, 2], [2, 4], [3, 1, 2], [1, 3, 1, 1]]), 2
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.leastBricks([[1], [1], [1]]), 3
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.leastBricks([[1]]), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.leastBricks([[1, 1, 1, 1]]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.leastBricks([[1, 2], [2, 1]]), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.leastBricks([[1, 1], [1, 1], [1, 1]]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.leastBricks([[2 ** 31 - 1, 2 ** 31 - 1], [2 ** 31 - 1, 2 ** 31 - 1]]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.leastBricks([[1, 2, 3], [3, 3], [2, 4]]), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.leastBricks([[1, 1, 1], [2, 1], [1, 2]]), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.leastBricks([[5, 5, 5], [10, 5], [5, 10]]), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.leastBricks([[1, 1, 1, 1, 1], [2, 3, 1, 1], [1, 4, 1, 1]]), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.leastBricks([[1, 2, 3, 4], [3, 3, 4], [2, 5, 3]]), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.leastBricks([[1] * 20000]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
