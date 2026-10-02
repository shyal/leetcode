"""
DRILL: Turn Knobs To A Total

You are DJing at a party and want to set the volume to V. The mixer
has two knobs, set at a and b, and you can turn each knob to any
position from 1 to limit. The volume is a + b. Return the fewest knobs
you must turn. The Solution already has band(a, b), which returns the
(lo, hi) of Turn One Dial: the smallest and largest volume one turn
can reach.

Example 1:

Input: a = 2, b = 4, limit = 4, V = 3
Output: 1
Explanation: turn the 4 down to 1.

Example 2:

Input: a = 2, b = 4, limit = 4, V = 6
Output: 0

Example 3:

Input: a = 2, b = 4, limit = 4, V = 2
Output: 2
Explanation: no single turn reaches a volume of 2.

Constraints:

    1 <= a, b <= limit <= 10^5
    2 <= V <= 2 * limit

    REQUIRED: O(1). NO loop over positions.
"""


# mu 0.7
# def numTurns(a: int, b: int, limit: int, V: int) -> int
#   def band(a, b)
#     (min(a, b) + 1, max(a, b) + limit)
#   if a + b == V
#     return 0
#   lo, hi = band(a, b)
#   1 if lo <= V <= hi else 2

class Solution:
    def numTurns(self, a: int, b: int, limit: int, V: int) -> int:
        def band(a, b):
            return (min(a, b) + 1, max(a, b) + limit)
        if a + b == V:
            return 0
        lo, hi = band(a, b)
        return 1 if lo <= V <= hi else 2


sol = Solution()
print(sol.numTurns(2, 4, 4, 3))
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
