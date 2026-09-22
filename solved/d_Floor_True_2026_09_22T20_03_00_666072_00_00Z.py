"""
DRILL: Floor True
TRAINS: binary-search-on-answer

Given integers lo and hi and a function ok, return the largest x in
[lo, hi] with ok(x) True. The function ok is True for every x up to some
value and False for every x above it. ok(lo) is True.

Example 1:

Input: lo = 1, hi = 100, ok = lambda x: x <= 37
Output: 37

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

    REQUIRED: must loop while lo <= hi and call ok O(log(hi - lo)) times.
    Every step must set lo = mid + 1 or hi = mid - 1. NO lo = mid, NO
    hi = mid, NO scan, NO first_true, NO last_true, NO first_false,
    NO last_false, NO bisect.

---

Learning

"""


class Solution:

    def floorTrue(self, lo: int, hi: int, ok: Callable[[int], bool]) -> int:
        while lo <= hi:
            mid = (lo + hi) // 2
            if ok(mid):
                lo = mid + 1
            else:
                hi = mid - 1
        return hi


sol = Solution()

print(sol.floorTrue(1, 100, lambda x: x <= 37))  # 37

assert sol.floorTrue(1, 100, lambda x: x <= 37) == 37
assert sol.floorTrue(1, 100, lambda x: x <= 100) == 100
assert sol.floorTrue(1, 100, lambda x: x <= 1) == 1
assert sol.floorTrue(1, 100, lambda x: x <= 50) == 50
assert sol.floorTrue(1, 100, lambda x: x <= 51) == 51
assert sol.floorTrue(7, 7, lambda x: True) == 7
assert sol.floorTrue(7, 8, lambda x: x <= 7) == 7
assert sol.floorTrue(7, 8, lambda x: x <= 8) == 8
assert sol.floorTrue(1, 10**9, lambda x: x <= 123456789) == 123456789
assert sol.floorTrue(1, 10**9, lambda x: x <= 1) == 1
calls = []
assert sol.floorTrue(1, 10**9, lambda x: calls.append(x) or x <= 5) == 5
assert len(calls) <= 31
assert avoids(
    Solution, first_true, last_true, first_false, last_false, bisect_left, bisect_right
)
