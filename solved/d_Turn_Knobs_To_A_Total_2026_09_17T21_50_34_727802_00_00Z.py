"""
DRILL: Turn Knobs To A Total

You are DJing at a party. The mixer has two knobs, set at a and b, and
each knob can be turned to any position from 1 to limit. The crowd
wants the two positions to add up to T. Return the fewest knobs you
must turn. The Solution already has band(a, b), which returns the
(lo, hi) of Turn One Dial: the smallest and largest total one turn can
reach.

Example 1:

Input: a = 2, b = 4, limit = 4, T = 3
Output: 1
Explanation: turn the 4 down to 1.

Example 2:

Input: a = 2, b = 4, limit = 4, T = 6
Output: 0

Example 3:

Input: a = 2, b = 4, limit = 4, T = 2
Output: 2
Explanation: no single turn reaches a total of 2.

Constraints:

    1 <= a, b <= limit <= 10^5
    2 <= T <= 2 * limit

    REQUIRED: O(1). NO loop over positions.
"""


class Solution:
    def numTurns(self, a: int, b: int, limit: int, T: int) -> int:
        band = lambda a, b: (min(a, b) + 1, max(a, b) + limit)
        lo, hi = band(a, b)
        if a + b == T:
            return 0
        if lo <= T <= hi:
            return 1
        return 2


sol = Solution()

print(sol.numTurns(2, 4, 4, 3))  # 1

assert sol.numTurns(2, 4, 4, 3) == 1
assert sol.numTurns(2, 4, 4, 6) == 0
assert sol.numTurns(2, 4, 4, 2) == 2
assert sol.numTurns(2, 4, 4, 8) == 1
assert sol.numTurns(2, 4, 4, 5) == 1
assert sol.numTurns(4, 2, 4, 3) == 1
assert sol.numTurns(3, 3, 3, 6) == 0
assert sol.numTurns(3, 3, 3, 4) == 1
assert sol.numTurns(3, 3, 3, 3) == 2
assert sol.numTurns(1, 1, 1, 2) == 0
assert sol.numTurns(1, 100000, 100000, 200000) == 1
assert sol.numTurns(7, 2, 9, 17) == 2
