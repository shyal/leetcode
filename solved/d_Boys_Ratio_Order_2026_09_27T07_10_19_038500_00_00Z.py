"""
DRILL: Boys Ratio Order
TRAINS: heap-top-k

Given a list classes, where classes[i] = [boys_i, students_i] is a class
with students_i students of whom boys_i are boys, return the classes in
increasing order of the ratio boys_i / students_i. No two classes share a
ratio.

Example 1:

Input: classes = [[3, 4], [1, 2], [2, 3]]
Output: [[1, 2], [2, 3], [3, 4]]
Explanation: The ratios are 0.75, 0.5 and 0.667.

Example 2:

Input: classes = [[1, 5], [4, 5]]
Output: [[1, 5], [4, 5]]

Example 3:

Input: classes = [[2, 2]]
Output: [[2, 2]]

Constraints:

    1 <= classes.length <= 10^5
    1 <= boys_i <= students_i <= 10^5
    All ratios boys_i / students_i are distinct.

    REQUIRED: must build a heap whose items carry the ratio as their first
    element, computed by a function, and pop the classes out in order.
    NO sort, NO sorted, NO key= argument.
"""


# mu 0.5
# def byRatio(classes: [[int]]) -> [[int]]
#   ret res, h = [], heap([[a/b, a, b] for (a, b) in classes])
#   while len h
#     res <- h.pop()[1:]

from heapq import heapify, heappop, heappush


class heap:
    class _Rev:
        __slots__ = "x"

        def __init__(self, x):
            self.x = x

        def __lt__(self, o):
            return o.x < self.x

    def __init__(self, items=(), type=min):
        self.rev = type is max
        self.h = [self.wrap(x) for x in items]
        heapify(self.h)

    def wrap(self, x):
        return heap._Rev(x) if self.rev else x

    def unwrap(self, x):
        return x.x if self.rev else x

    def push(self, x):
        heappush(self.h, self.wrap(x))

    append = push

    def pop(self):
        return self.unwrap(heappop(self.h))

    def peek(self):
        return self.unwrap(self.h[0])

    def __len__(self):
        return len(self.h)

    def __iter__(self):
        return (self.unwrap(x) for x in self.h)


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
    def byRatio(self, classes: list[list[int]]) -> list[list[int]]:
        _in_classes, classes = classes, Grid(classes)
        _w_classes = classes
        try:
            res, h = [], heap([[a / b, a, b] for (a, b) in classes])
            while len(h):
                res.append(h.pop()[1:])
            return res
        finally:
            _in_classes[:] = _w_classes


sol = Solution()
print(sol.byRatio([[3, 4], [1, 2], [2, 3]]))
assert sol.byRatio([[3, 4], [1, 2], [2, 3]]) == [[1, 2], [2, 3], [3, 4]]
assert sol.byRatio([[1, 5], [4, 5]]) == [[1, 5], [4, 5]]
assert sol.byRatio([[2, 2]]) == [[2, 2]]
assert sol.byRatio([[1, 2], [1, 3], [1, 4]]) == [[1, 4], [1, 3], [1, 2]]
assert sol.byRatio([[1, 4], [1, 3], [1, 2]]) == [[1, 4], [1, 3], [1, 2]]
assert sol.byRatio([[5, 5], [1, 100], [50, 99]]) == [[1, 100], [50, 99], [5, 5]]
big = [[1, s] for s in range(2, 100002)]
assert sol.byRatio(big) == big[::-1]
src = open(__file__).read().split('sol = Solution()')[0]
assert 'sort' not in src.split('"""')[2] and 'key=' not in src.split('"""')[2]
