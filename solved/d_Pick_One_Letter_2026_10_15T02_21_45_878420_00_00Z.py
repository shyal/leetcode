"""
DRILL: Pick One Letter
TRAINS: dp-1d-rolling

Given a string s and a letter c, return an array ways of length len(s) + 1.
The value ways[i] is the number of ways to pick one c from the first i
characters of s.

Example 1:

Input: s = "babcb", c = "b"
Output: [0, 1, 1, 2, 2, 3]
Explanation: the first 4 characters "babc" hold two b's, so ways[4] = 2.

Example 2:

Input: s = "bbb", c = "b"
Output: [0, 1, 2, 3]

Example 3:

Input: s = "xyz", c = "b"
Output: [0, 0, 0, 0]

Constraints:

    1 <= len(s) <= 10^5
    s and c consist of lowercase English letters, and len(c) == 1.

    REQUIRED: O(len(s)) time, each ways[i] built from ways[i - 1].
    Recounting every prefix from scratch is the fail. NO s.count, NO slicing.
"""


# mu 0.10
# class Solution
#   @as_list
#   def countPicks(s: str, c: str) -> [int]
#     count = 0
#     for ch in s
#       yield count
#       if ch == c
#         count += 1
#     yield count
#
#

from functools import wraps


def as_list(f):

    @wraps(f)
    def wrapper(*args, **kwargs):
        return list(f(*args, **kwargs))
    return wrapper


class Solution:
    @as_list
    def countPicks(self, s: str, c: str) -> list[int]:
        count = 0
        for ch in s:
            yield count
            if ch == c:
                count += 1
        yield count


sol = Solution()
print(sol.countPicks('babcb', 'b'))
_l, _r = sol.countPicks('babcb', 'b'), [0, 1, 1, 2, 2, 3]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.countPicks('bbb', 'b'), [0, 1, 2, 3]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.countPicks('xyz', 'b'), [0, 0, 0, 0]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.countPicks('a', 'a'), [0, 1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.countPicks('a', 'b'), [0, 0]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.countPicks('abcab', 'a'), [0, 1, 1, 1, 2, 2]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.countPicks('xxxxb', 'b'), [0, 0, 0, 0, 0, 1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.countPicks('z' * 100000, 'z')[-1], 100000
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
