"""
EPI 4.11 Rectangle intersection

Given two rectangles r1 and r2 with sides parallel to the axes, return
the rectangle that is their intersection. Rect(x, y, width, height) has
its lower-left corner at (x, y) and its upper-right corner at
(x + width, y + height). Two rectangles that touch along an edge or at a
corner intersect in a rectangle of width 0 or height 0. When r1 and r2
have no point in common, return Rect(0, 0, -1, -1).

Example 1:

Input: r1 = Rect(0, 0, 4, 3), r2 = Rect(2, 1, 5, 5)
Output: Rect(x=2, y=1, width=2, height=2)
Explanation: the intersection runs from x = 2 to x = 4 and from y = 1
to y = 3.

    y
    6 |     +---------+
      |     |   r2    |
    3 +-----+---+     |
      |  r1 |///|     |
    1 |     +---+-----+
    0 +---------+-------- x
      0     2   4     7

Example 2:

Input: r1 = Rect(0, 0, 2, 2), r2 = Rect(2, 0, 3, 1)
Output: Rect(x=2, y=0, width=0, height=1)
Explanation: the rectangles touch along the edge x = 2, from y = 0 to
y = 1.

Example 3:

Input: r1 = Rect(0, 0, 1, 1), r2 = Rect(3, 3, 1, 1)
Output: Rect(x=0, y=0, width=-1, height=-1)

Constraints:

    -10^9 <= x, y <= 10^9
    0 <= width, height <= 10^9

    REQUIRED: O(1) time. NO loop.
"""

from collections import namedtuple

Rect = namedtuple("Rect", ("x", "y", "width", "height"))


class Solution:
    def intersect_rectangle(self, r1: Rect, r2: Rect) -> Rect:
        pass


sol = Solution()

print(sol.intersect_rectangle(Rect(0, 0, 4, 3), Rect(2, 1, 5, 5)))  # Rect(x=2, y=1, width=2, height=2)

# assert sol.intersect_rectangle(Rect(0, 0, 4, 3), Rect(2, 1, 5, 5)) == Rect(2, 1, 2, 2)
# assert sol.intersect_rectangle(Rect(2, 1, 5, 5), Rect(0, 0, 4, 3)) == Rect(2, 1, 2, 2)
# assert sol.intersect_rectangle(Rect(0, 0, 2, 2), Rect(2, 0, 3, 1)) == Rect(2, 0, 0, 1)
# assert sol.intersect_rectangle(Rect(0, 0, 1, 1), Rect(3, 3, 1, 1)) == Rect(0, 0, -1, -1)
# assert sol.intersect_rectangle(Rect(0, 0, 1, 1), Rect(1, 1, 1, 1)) == Rect(1, 1, 0, 0)
# assert sol.intersect_rectangle(Rect(0, 0, 1, 1), Rect(2, 0, 1, 1)) == Rect(0, 0, -1, -1)
# assert sol.intersect_rectangle(Rect(0, 0, 1, 1), Rect(0, 2, 1, 1)) == Rect(0, 0, -1, -1)
# assert sol.intersect_rectangle(Rect(0, 0, 10, 10), Rect(3, 4, 2, 1)) == Rect(3, 4, 2, 1)
# assert sol.intersect_rectangle(Rect(0, 0, 5, 5), Rect(0, 0, 5, 5)) == Rect(0, 0, 5, 5)
# assert sol.intersect_rectangle(Rect(0, 0, 10, 2), Rect(4, -5, 2, 20)) == Rect(4, 0, 2, 2)
# assert sol.intersect_rectangle(Rect(-5, -5, 3, 3), Rect(-4, -4, 10, 10)) == Rect(-4, -4, 2, 2)
# assert sol.intersect_rectangle(Rect(0, 0, 0, 0), Rect(0, 0, 3, 3)) == Rect(0, 0, 0, 0)
# assert sol.intersect_rectangle(Rect(5, 5, 0, 0), Rect(0, 0, 3, 3)) == Rect(0, 0, -1, -1)
# assert sol.intersect_rectangle(Rect(-10 ** 9, -10 ** 9, 10 ** 9, 10 ** 9), Rect(0, 0, 10 ** 9, 10 ** 9)) == Rect(0, 0, 0, 0)
