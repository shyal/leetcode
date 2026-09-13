"""
DRILL: Forklift Moves
SNIPPET: lcdirs

Given an integer s, return the moves of a forklift that drives s bays
along exactly one aisle. A move is a pair (dr, dc): dr is the change in
row, dc the change in column. Return the four moves in increasing order.
Build the candidate pairs with itertools.product and keep the moves with
filter.

Example 1:

Input: s = 1
Output: [(-1, 0), (0, -1), (0, 1), (1, 0)]

Example 2:

Input: s = 3
Output: [(-3, 0), (0, -3), (0, 3), (3, 0)]
Explanation: (3, 3) drives along both aisles, so it is not a move.

Constraints:

    1 <= s <= 100

    REQUIRED: the four pairs come out of one product call over the three
    steps -s, 0, s. NO literal list of four pairs, NO nested for loops.
"""


class Solution:
    def moves(self, s: int) -> list[tuple[int, int]]:
        pass


sol = Solution()

print(sol.moves(1))  # [(-1, 0), (0, -1), (0, 1), (1, 0)]

# assert sol.moves(1) == [(-1, 0), (0, -1), (0, 1), (1, 0)]
# assert sol.moves(3) == [(-3, 0), (0, -3), (0, 3), (3, 0)]
# assert sol.moves(100) == [(-100, 0), (0, -100), (0, 100), (100, 0)]
# assert all(isinstance(d, tuple) for d in sol.moves(2))
