"""
DRILL: Count Pairs

Take every pair of positions i < j in xs. The pair counts when
by(xs[i]) == want(xs[j]). The function by gives the key a number is stored
under, and the function want gives the key a number looks for. Return how
many pairs count.

Example 1:

Input: xs = [3, 1, 4, 6, 3], by = lambda x: x, want = lambda x: x - 2
Output: 2
Explanation: The 6 looks for 4, and a 4 is earlier. The last 3 looks for
1, and a 1 is earlier. The first 3 looks for 1 too, but no 1 is earlier.

Example 2:

Input: xs = [2, 9, 4, 16, 7, 23], by = lambda x: x % 7, want = lambda x: x % 7
Output: 6
Explanation: 2, 9, 16 and 23 all have key 2. Four numbers make 6 pairs.

Constraints:

    0 <= len(xs) <= 10^5
    -10^9 <= xs[i] <= 10^9
    by and want each run in O(1).

    REQUIRED: O(n), one pass over xs. NO enumeration of index pairs.
---
Learning
"""


# mu 0.10
# class Solution
#   def countPairs(xs: [int], by: int -> int, want: int -> int) -> int
#     c = counter()
#     sum for x in xs
#       got = c[want(x)]
#       c[by(x)] += 1
#       got

from collections import Counter
from typing import Callable


class Solution:
    def countPairs(self, xs: list[int], by: Callable[[int], int], want: Callable[[int], int]) -> int:
        c = Counter()
        acc = 0
        for x in xs:
            got = c[want(x)]
            c[by(x)] += 1
            acc += got
        return acc


sol = Solution()
print(sol.countPairs([3, 1, 4, 6, 3], lambda x: x, lambda x: x - 2))
_l, _r = sol.countPairs([3, 1, 4, 6, 3], lambda x: x, lambda x: x - 2), 2
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.countPairs([2, 9, 4, 16, 7, 23], lambda x: x % 7, lambda x: x % 7), 6
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.countPairs([], lambda x: x, lambda x: x), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.countPairs([5], lambda x: x, lambda x: x), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.countPairs([4, 4], lambda x: x, lambda x: x), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.countPairs([2, 2, 2], lambda x: x, lambda x: x), 3
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.countPairs([1, 3], lambda x: x, lambda x: x - 2), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.countPairs([3, 1], lambda x: x, lambda x: x - 2), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.countPairs([1, 5, 5, 5, 3], lambda x: x, lambda x: x - 2), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.countPairs([1, 4, 5, 9, 10], lambda x: x % 5, lambda x: -x % 5), 3
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.countPairs([7] * 10 ** 5, lambda x: x, lambda x: x), 4999950000
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.countPairs(list(range(0, 10 ** 5)), lambda x: x, lambda x: x - 1), 99999
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
assert avoids(Solution, count_pairs)
