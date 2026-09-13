"""
DRILL: Forklift Moves
SNIPPET: lcdirs

Given an integer s, return the four offsets (dr, dc) with dr and dc in
{-s, 0, s} and exactly one of them nonzero, in increasing order. Build
the candidates with itertools.product and keep the four with filter.

Example 1:

Input: s = 1
Output: [(-1, 0), (0, -1), (0, 1), (1, 0)]

Example 2:

Input: s = 3
Output: [(-3, 0), (0, -3), (0, 3), (3, 0)]

Constraints:

    1 <= s <= 100

    REQUIRED: one product call over -s, 0, s. NO literal list of four
    pairs, NO nested for loops.
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
