"""
DRILL: Sprinkler On A Lawn

Given a lawn of m rows and n columns of tiles and a sprinkler on tile
(r, c), return the tiles the sprinkler wets. It wets the tile above, the
tile to the left, the tile to the right and the tile below, in that
order, and only tiles on the lawn. Rows and columns are numbered from 0.
Build each neighbour from an offset with a generator expression and test
the bounds on the built pair, never on the offset.

Example 1:

Input: m = 3, n = 3, r = 1, c = 1
Output: [(0, 1), (1, 0), (1, 2), (2, 1)]

Example 2:

Input: m = 3, n = 3, r = 0, c = 0
Output: [(0, 1), (1, 0)]
Explanation: (-1, 0) and (0, -1) are off the lawn.

Example 3:

Input: m = 1, n = 1, r = 0, c = 0
Output: []

Constraints:

    1 <= m, n <= 1000
    0 <= r < m
    0 <= c < n

    REQUIRED: one pass over the four offsets. NO try/except around an
    index, NO if per offset.
"""


class Solution:
    def wets(self, m: int, n: int, r: int, c: int) -> list[tuple[int, int]]:
        pass


sol = Solution()

print(sol.wets(3, 3, 1, 1))  # [(0, 1), (1, 0), (1, 2), (2, 1)]

# assert sol.wets(3, 3, 1, 1) == [(0, 1), (1, 0), (1, 2), (2, 1)]
# assert sol.wets(3, 3, 0, 0) == [(0, 1), (1, 0)]
# assert sol.wets(1, 1, 0, 0) == []
# assert sol.wets(3, 3, 2, 2) == [(1, 2), (2, 1)]
# assert sol.wets(1, 4, 0, 2) == [(0, 1), (0, 3)]
# assert sol.wets(4, 1, 2, 0) == [(1, 0), (3, 0)]
# assert sol.wets(1000, 1000, 999, 0) == [(998, 0), (999, 1)]
