"""
DRILL: One From Each

Given a list of groups, where each group is a list of lowercase letters,
return every string built by taking one letter from group 0, then one
from group 1, and so on to the last group. The strings may come back in
any order.

Example 1:

Input: groups = [["a", "b", "c"], ["x", "y", "z"]]
Output: ["ax", "ay", "az", "bx", "by", "bz", "cx", "cy", "cz"]
Explanation: the first letter of every string comes from group 0 and the
second from group 1. Three choices for each, so there are nine strings.

Example 2:

Input: groups = [["x", "y", "z"]]
Output: ["x", "y", "z"]

Constraints:

    1 <= len(groups) <= 8
    1 <= len(groups[i]) <= 5
    Every group holds distinct lowercase letters.

    REQUIRED: the candidates at depth d are the letters of groups[d] and
    nothing else. One list holds the letters chosen so far, for the
    whole run. NO itertools, NO `path + [x]`, NO building the string on
    the way down. Join the list into a string only when the last group
    has been chosen from.
"""


# mu 0.12
# class Solution
#   def combos(groups: [[str]]) -> [str]
#     # # a
#     # #  x
#     # #  y
#     def helper(i)
#       if i == len groups
#         res <- ''.join(path[:])
#         return
#       for >j in groups[i]
#         path <- groups[i][j]
#         helper(i + 1)
#         path .
#     ret res, path = [], []
#     helper(0)

class Grid(list):
    """A list of rows that also takes a (row, col) pair as an index."""

    def __getitem__(self, k):
        if type(k) is tuple:
            return list.__getitem__(self, k[0])[k[1]]
        return list.__getitem__(self, k)

    def __setitem__(self, k, v):
        if type(k) is tuple:
            list.__getitem__(self, k[0])[k[1]] = v
        else:
            list.__setitem__(self, k, v)


class Solution:
    def combos(self, groups: list[list[str]]) -> list[str]:
        _in_groups, groups = groups, Grid(groups)
        _w_groups = groups
        try:
            def helper(i):
                if i == len(groups):
                    res.append(''.join(path[:]))
                    return
                for j in range(len(groups[i])):
                    path.append(groups[i][j])
                    helper(i + 1)
                    path.pop()
            res, path = [], []
            helper(0)
            return res
        finally:
            _in_groups[:] = _w_groups


sol = Solution()
print(sol.combos([['a', 'b', 'c'], ['x', 'y', 'z']]))
_l, _r = sorted(sol.combos([['a', 'b', 'c'], ['x', 'y', 'z']])), ['ax', 'ay', 'az', 'bx', 'by', 'bz', 'cx', 'cy', 'cz']
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sorted(sol.combos([['x', 'y', 'z']])), ['x', 'y', 'z']
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sorted(sol.combos([['a'], ['b'], ['c']])), ['abc']
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
res = sol.combos([['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i']])
assert len(res) == 27 and len(set(res)) == 27
assert all((len(s) == 3 for s in res))
res = sol.combos([['a', 'b']] * 8)
assert len(res) == 256 and len(set(res)) == 256
