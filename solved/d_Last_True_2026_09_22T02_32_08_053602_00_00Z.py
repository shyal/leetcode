"""
DRILL: Last True

Given integers lo and hi and a function ok, return the largest x in
[lo, hi] with ok(x) True. The function ok is True for every x up to some
value and False for every x above it. ok(lo) is True.

Example 1:

Input: lo = 1, hi = 100, ok = lambda x: x * x <= 50
Output: 7
Explanation: 7 * 7 = 49 is at most 50, 8 * 8 = 64 is not.

Example 2:

Input: lo = 1, hi = 100, ok = lambda x: x <= 100
Output: 100

Example 3:

Input: lo = 1, hi = 100, ok = lambda x: x <= 1
Output: 1

Constraints:

    1 <= lo <= hi <= 10^9
    ok(lo) is True.
    ok is True for a prefix of [lo, hi] and False for the rest.

    REQUIRED: must write the loop over lo and hi yourself and call ok
    O(log(hi - lo)) times. NO scan from hi. NO first_true, NO last_true,
    NO first_false, NO last_false, NO bisect. The loop must end on every
    input; a step that leaves lo and hi unchanged is a fail.
"""


class Solution:

    def lastTrue(self, lo: int, hi: int, ok: Callable[[int], bool]) -> int:
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if ok(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo


sol = Solution()

print(sol.lastTrue(1, 100, lambda x: x * x <= 50))  # 7

assert sol.lastTrue(1, 100, lambda x: x * x <= 50) == 7
assert sol.lastTrue(1, 100, lambda x: x <= 100) == 100
assert sol.lastTrue(1, 100, lambda x: x <= 1) == 1
assert sol.lastTrue(1, 100, lambda x: x <= 50) == 50
assert sol.lastTrue(1, 100, lambda x: x <= 51) == 51
assert sol.lastTrue(7, 7, lambda x: True) == 7
assert sol.lastTrue(7, 8, lambda x: x <= 7) == 7
assert sol.lastTrue(7, 8, lambda x: x <= 8) == 8
assert sol.lastTrue(1, 10**9, lambda x: x <= 123456789) == 123456789
assert sol.lastTrue(1, 10**9, lambda x: x <= 1) == 1
calls = []
assert sol.lastTrue(1, 10**9, lambda x: calls.append(x) or x <= 5) == 5
assert len(calls) <= 31
assert avoids(
    Solution, first_true, last_true, first_false, last_false, bisect_left, bisect_right
)
