"""
DRILL: First False

Given integers lo and hi and a function ok, return the smallest x in
[lo, hi] with ok(x) False. The function ok is True for every x below
some value and False for that value and every x above it. ok(hi) is False.

Example 1:

Input: lo = 1, hi = 100, ok = lambda x: x * x <= 50
Output: 8
Explanation: 7 * 7 = 49 is at most 50, 8 * 8 = 64 is not.

Example 2:

Input: lo = 1, hi = 100, ok = lambda x: x < 1
Output: 1

Example 3:

Input: lo = 1, hi = 100, ok = lambda x: x < 100
Output: 100

Constraints:

    1 <= lo <= hi <= 10^9
    ok(hi) is False.
    ok is True for a prefix of [lo, hi] and False for the rest.

    REQUIRED: must write the loop over lo and hi yourself and call ok
    O(log(hi - lo)) times. NO scan from lo. NO first_true, NO last_true,
    NO first_false, NO last_false, NO bisect. The loop must end on every
    input; a step that leaves lo and hi unchanged is a fail.
"""


# mu source (current.mu), the candidate's solution. The Python
# under it is the transpiler's output, and it is what ran.
#
# def firstFalse(lo: int, hi: int, ok: int -> bool) -> int
#   while lo < hi
#     mid = (lo + hi) // 2
#     if ok(mid)
#       lo = mid + 1
#     else
#       hi = mid
#   lo

from typing import Callable


class Solution:
    def firstFalse(self, lo: int, hi: int, ok: Callable[[int], bool]) -> int:
        while lo < hi:
            mid = (lo + hi) // 2
            if ok(mid):
                lo = mid + 1
            else:
                hi = mid
        return lo


sol = Solution()
print(sol.firstFalse(1, 100, lambda x: x * x <= 50))
assert sol.firstFalse(1, 100, lambda x: x * x <= 50) == 8
assert sol.firstFalse(1, 100, lambda x: x < 1) == 1
assert sol.firstFalse(1, 100, lambda x: x < 100) == 100
assert sol.firstFalse(1, 100, lambda x: x < 50) == 50
assert sol.firstFalse(1, 100, lambda x: x < 51) == 51
assert sol.firstFalse(7, 7, lambda x: False) == 7
assert sol.firstFalse(7, 8, lambda x: x < 8) == 8
assert sol.firstFalse(7, 8, lambda x: x < 7) == 7
assert sol.firstFalse(1, 10 ** 9, lambda x: x < 123456789) == 123456789
assert sol.firstFalse(1, 10 ** 9, lambda x: x < 10 ** 9) == 10 ** 9
calls = []
assert sol.firstFalse(1, 10 ** 9, lambda x: calls.append(x) or x < 5) == 5
assert len(calls) <= 31
assert avoids(Solution, first_true, last_true, first_false, last_false, bisect_left, bisect_right)
