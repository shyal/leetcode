"""
DRILL: Build Parents

Given n, the number of employees, labeled 0 to n - 1, return the list
parent, where parent[i] is the manager of employee i. Nobody has been
assigned a manager yet, so every employee is their own manager.

Example 1:

Input: n = 4
Output: [0, 1, 2, 3]

Example 2:

Input: n = 1
Output: [0]

Constraints:

    1 <= n <= 1000

    REQUIRED: must run in O(n) time and return a list the caller can
    assign into. NO dict; NO range object.
"""


# mu 0.11
# class Solution
#   def buildParent(n: int) -> [int]
#     [*0..<n]

class Solution:
    def buildParent(self, n: int) -> list[int]:
        return [*range(0, n)]


sol = Solution()
print(sol.buildParent(4))
_l, _r = sol.buildParent(4), [0, 1, 2, 3]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.buildParent(1), [0]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
parent = sol.buildParent(3)
parent[1] = 0
_l, _r = parent, [0, 0, 2]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
