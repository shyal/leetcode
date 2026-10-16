"""
DRILL: Find Roots

Given parent, a list where parent[i] is the manager of employee i, return
a function find. An employee who is their own manager is a head. The call
find(x) follows managers from x and returns the head it reaches.
Management chains never contain cycles, so the walk always reaches a head.
The function must read parent at call time: the tests change entries after
find is built and call it again.

Example 1:

Input: parent = [0, 0, 1, 3]
Output: find(2) == 0, find(1) == 0, find(3) == 3
Explanation: employee 2 reports to 1, who reports to 0, who is a head.
Employee 3 is a head.

Example 2:

Input: parent = [1, 2, 3, 4, 4]
Output: find(0) == 4

Constraints:

    1 <= len(parent) <= 1000
    parent is free of cycles whenever find is called

    REQUIRED: must run in O(d) time per call, where d is the number of
    managers walked. NO copy of parent; NO heads computed in advance.
"""


# mu 0.11
# class Solution
#   def buildFind(parent: [int]) -> int -> int
#     def find(x)
#       if x == parent[x]
#         return x
#       find(parent[x])
#     find

from typing import Callable


class Solution:
    def buildFind(self, parent: list[int]) -> Callable[[int], int]:
        def find(x):
            if x == parent[x]:
                return x
            return find(parent[x])
        return find


sol = Solution()
print(sol.buildFind([0, 0, 1, 3])(2))
find = sol.buildFind([0, 0, 1, 3])
_l, _r = [find(x) for x in range(0, 4)], [0, 0, 0, 3]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
find = sol.buildFind([1, 2, 3, 4, 4])
_l, _r = find(0), 4
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = find(4), 4
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
parent = [0, 1, 2, 3]
find = sol.buildFind(parent)
_l, _r = [find(x) for x in range(0, 4)], [0, 1, 2, 3]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
parent[1] = 0
parent[2] = 1
_l, _r = find(2), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = find(3), 3
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
find = sol.buildFind([0])
_l, _r = find(0), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
