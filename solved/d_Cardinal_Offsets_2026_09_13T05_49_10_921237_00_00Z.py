"""
DRILL: Cardinal Offsets
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

---

learning

"""


class Solution:
    def offsets(self, s: int) -> list[tuple[int, int]]:
        prod = product((-s, 0, s), repeat=2)
        lam = lambda d: abs(d[0]) + abs(d[1]) == s
        return [*filter(lam, prod)]


sol = Solution()

print(sol.offsets(1))  # [(-1, 0), (0, -1), (0, 1), (1, 0)]

assert sol.offsets(1) == [(-1, 0), (0, -1), (0, 1), (1, 0)]
assert sol.offsets(3) == [(-3, 0), (0, -3), (0, 3), (3, 0)]
assert sol.offsets(100) == [(-100, 0), (0, -100), (0, 100), (100, 0)]
assert all(isinstance(d, tuple) for d in sol.offsets(2))
