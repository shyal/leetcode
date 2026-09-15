"""
DRILL: First True

Given integers lo and hi and a function ok, return the smallest x in
[lo, hi] with ok(x) True. The function ok is False for every x below
some value and True for that value and every x above it. ok(hi) is True.

Example 1:

Input: lo = 1, hi = 100, ok = lambda x: x * x >= 50
Output: 8
Explanation: 7 * 7 = 49 is below 50, 8 * 8 = 64 is not.

Example 2:

Input: lo = 1, hi = 100, ok = lambda x: x >= 1
Output: 1

Example 3:

Input: lo = 1, hi = 100, ok = lambda x: x >= 100
Output: 100

Constraints:

    1 <= lo <= hi <= 10^9
    ok(hi) is True.
    ok is False for a prefix of [lo, hi] and True for the rest.

    REQUIRED: must call ok O(log(hi - lo)) times. NO scan from lo. The
    loop must end on every input; a step that leaves lo and hi unchanged
    is a fail.
"""


class Solution:

    def firstTrue(self, lo: int, hi: int, ok: Callable[[int], bool]) -> int:
        while lo < hi:
            mid = (lo + hi) // 2
            if ok(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo


sol = Solution()

print(sol.firstTrue(1, 100, lambda x: x * x >= 50))  # 8

assert sol.firstTrue(1, 100, lambda x: x * x >= 50) == 8
assert sol.firstTrue(1, 100, lambda x: x >= 1) == 1
assert sol.firstTrue(1, 100, lambda x: x >= 100) == 100
assert sol.firstTrue(1, 100, lambda x: x >= 50) == 50
assert sol.firstTrue(1, 100, lambda x: x >= 51) == 51
assert sol.firstTrue(7, 7, lambda x: True) == 7
assert sol.firstTrue(7, 8, lambda x: x >= 8) == 8
assert sol.firstTrue(7, 8, lambda x: x >= 7) == 7
assert sol.firstTrue(1, 10**9, lambda x: x >= 123456789) == 123456789
assert sol.firstTrue(1, 10**9, lambda x: x >= 10**9) == 10**9
calls = []
assert sol.firstTrue(1, 10**9, lambda x: calls.append(x) or x >= 5) == 5
assert len(calls) <= 31
