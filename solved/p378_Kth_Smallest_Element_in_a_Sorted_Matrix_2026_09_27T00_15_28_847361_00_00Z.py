"""
URL: https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/description/?envType=problem-list-v2&envId=vn57k9wr

378. Kth Smallest Element in a Sorted Matrix

Given an n x n matrix where each of the rows and columns is sorted in ascending order, return the kth smallest element in the matrix.

Note that it is the kth smallest element in the sorted order, not the kth distinct element.

You must find a solution with a memory complexity better than O(n^2).

Example 1:

Input: matrix = [[1,5,9],[10,11,13],[12,13,15]], k = 8
Output: 13
Explanation: The elements in the matrix are [1,5,9,10,11,12,13,13,15], and the 8th smallest number is 13

Example 2:

Input: matrix = [[-5]], k = 1
Output: -5

Constraints:

    n == matrix.length == matrix[i].length
    1 <= n <= 300
    -10^9 <= matrix[i][j] <= 10^9
    All the rows and columns of matrix are guaranteed to be sorted in non-decreasing order.
    1 <= k <= n^2

Follow up:

    Could you solve the problem with a constant memory (i.e., O(1) memory complexity)?
    Could you solve the problem in O(n) time complexity? The solution may be too advanced for an interview but you may find reading this paper fun.
---
recognition failure.. on something i solved 13 days ago
learning

LEETCODE: Accepted (119 ms, 24.7 MB)
"""


# mu 0.5
# def kthSmallest(m: [[int]], k: int) -> int
#   h = heap([], type=max)
#   for c in cells(m)
#     h <- m[c]
#     if len h > k
#       h .
#   h.peek()

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


def _holds(v, eq=None, lt=None, lte=None, gt=None, gte=None):
    return (
        (eq is None or v == eq)
        and (lt is None or v < lt)
        and (lte is None or v <= lte)
        and (gt is None or v > gt)
        and (gte is None or v >= gte)
    )


def cells(grid, start=0, val=None, eq=None, lt=None, lte=None, gt=None, gte=None):
    eq = val if eq is None else eq
    for i in range(start, len(grid)):
        for j in range(start, len(grid[0])):
            if _holds(grid[i][j], eq, lt, lte, gt, gte):
                yield i, j


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
    def kthSmallest(self, m: list[list[int]], k: int) -> int:
        _in_m, m = m, Grid(m)
        _w_m = m
        try:
            h = heap([], type=max)
            for c in cells(m):
                h.append(m[c])
                if len(h) > k:
                    h.pop()
            return h.peek()
        finally:
            _in_m[:] = _w_m


sol = Solution()
print(sol.kthSmallest([[1, 5, 9], [10, 11, 13], [12, 13, 15]], 8))
assert sol.kthSmallest([[1, 5, 9], [10, 11, 13], [12, 13, 15]], 8) == 13
assert sol.kthSmallest([[-5]], 1) == -5
assert Solution().kthSmallest([[1]], 1) == 1
assert Solution().kthSmallest([[1, 2], [1, 3]], 2) == 1
assert Solution().kthSmallest([[1, 2], [1, 3]], 3) == 2
assert Solution().kthSmallest([[1, 1, 1], [1, 1, 1], [1, 1, 1]], 5) == 1
assert Solution().kthSmallest([[-10 ** 9, -10 ** 9 + 1], [-10 ** 9 + 2, -10 ** 9 + 3]], 3) == -999999998
assert Solution().kthSmallest([[10 ** 9 - 3, 10 ** 9 - 2], [10 ** 9 - 1, 10 ** 9]], 4) == 1000000000
assert Solution().kthSmallest([[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6], [4, 5, 6, 7]], 10) == 4
assert Solution().kthSmallest([[1, 2, 2, 2], [2, 2, 2, 3], [2, 2, 3, 4], [2, 3, 4, 5]], 7) == 2
assert Solution().kthSmallest([[1, 3, 5], [6, 7, 12], [11, 14, 14]], 6) == 11
assert Solution().kthSmallest([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 9) == 9
assert Solution().kthSmallest([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 1) == 1
assert Solution().kthSmallest([[1, 1, 2], [1, 2, 3], [2, 3, 4]], 4) == 2
