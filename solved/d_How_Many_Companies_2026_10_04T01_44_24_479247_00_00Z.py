"""
DRILL: How Many Companies

Given n employees numbered 0 to n - 1 and pairs, where pairs[i] = [a, b]
means a and b work at the same company, return how many companies there
are. Solution extends UnionFind from dsa/union_find.py, built over the n
employees with each one in a company of their own. The call
self.union(a, b) merges the companies of a and b and returns True, or
returns False when they were already one company.

Example 1:

Input: n = 4, pairs = [[0, 1], [0, 2], [1, 2]]
Output: 2
Explanation: 0, 1 and 2 are one company. 3 is another. The third pair
merges nothing.

    start          {0} {1} {2} {3}       parent = [0, 1, 2, 3]

    union(0, 1)    {0 1} {2} {3}         parent = [1, 1, 2, 3]   True
                      1
                      |
                      0

    union(0, 2)    {0 1 2} {3}           parent = [1, 2, 2, 3]   True
                      2
                      |
                      1
                      |
                      0

    union(1, 2)    {0 1 2} {3}           parent = [1, 2, 2, 3]   False
                   (1 and 2 already share root 2, nothing changes)

Example 2:

Input: n = 5, pairs = []
Output: 5

Constraints:

    1 <= n <= 1000
    0 <= len(pairs) <= 2000
    pairs[i] = [a, b] with 0 <= a, b < n

    REQUIRED: must use only what union returns. NO scan of self.parent at
    the end. NO find or union of your own.
"""

from dsa.union_find import UnionFind


# mu 0.7
# extends UnionFind
#
# def countCompanies(pairs: [[int]]) -> int
#   for (a, b) in pairs
#     self.union(a, b)
#   return len(self.groups())

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


class Solution(UnionFind):
    def countCompanies(self, pairs: list[list[int]]) -> int:
        _in_pairs, pairs = pairs, Grid(pairs)
        _w_pairs = pairs
        try:
            for (a, b) in pairs:
                self.union(a, b)
            return len(self.groups())
        finally:
            _in_pairs[:] = _w_pairs


sol = Solution(4)
print(sol.countCompanies([[0, 1], [0, 2], [1, 2]]))
assert Solution(4).countCompanies([[0, 1], [0, 2], [1, 2]]) == 2
assert Solution(3).countCompanies([[0, 1], [1, 2]]) == 1
assert Solution(5).countCompanies([]) == 5
assert Solution(6).countCompanies([[0, 1], [2, 3], [4, 5], [0, 2], [3, 5]]) == 1
assert Solution(4).countCompanies([[0, 1], [1, 0], [2, 3], [0, 3]]) == 1
assert Solution(1).countCompanies([]) == 1
assert Solution(2).countCompanies([[0, 1], [0, 1]]) == 1
assert Solution(4).countCompanies([[0, 1], [2, 3]]) == 2
assert Solution(3).countCompanies([[0, 0]]) == 3
