"""
URL: https://leetcode.com/problems/h-index-ii/description/?envType=problem-list-v2&envId=vn57k9wr

275. H-Index II

Given an array of integers citations where citations[i] is the number of citations a researcher received for their i-th paper and citations is sorted in non-descending order, return the researcher's h-index.

According to the definition of h-index on Wikipedia: The h-index is defined as the maximum value of h such that the given researcher has published at least h papers that have each been cited at least h times.

You must write an algorithm that runs in logarithmic time.

Example 1:

Input: citations = [0,1,3,5,6]
Output: 3
Explanation: [0,1,3,5,6] means the researcher has 5 papers in total and each of them had received 0, 1, 3, 5, 6 citations respectively.
Since the researcher has 3 papers with at least 3 citations each and the remaining two with no more than 3 citations each, their h-index is 3.

Example 2:

Input: citations = [1,2,100]
Output: 2

Constraints:

    n == citations.length
    1 <= n <= 10^5
    0 <= citations[i] <= 1000
    citations is sorted in ascending order.
---
took me a while to understand that the h-index is the number of papers with at least that amount of citations
Learning

LEETCODE: Accepted (0 ms, 24.9 MB)
"""


# mu 0.7
# def hIndex(citations: [int]) -> int
#   n = len(citations)
#   n - first_true(0, n - 1, i -> citations[i] >= n - i)

from bisect import bisect_left


def first_true(lo, hi, ok):
    return lo + bisect_left(range(lo, hi + 1), True, key=ok)


class Solution:
    def hIndex(self, citations: list[int]) -> int:
        n = len(citations)
        return n - first_true(0, n - 1, lambda i: citations[i] >= n - i)


sol = Solution()
print(sol.hIndex([0, 1, 3, 5, 6]))
_l, _r = sol.hIndex([0, 1, 3, 5, 6]), 3
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.hIndex([1, 2, 100]), 2
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.hIndex([0]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.hIndex([1000]), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.hIndex([0, 0, 0, 0, 0]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.hIndex([1000, 1000, 1000, 1000, 1000]), 5
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.hIndex([0, 0, 1, 1, 1]), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.hIndex([0, 0, 0, 0, 5]), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.hIndex([0, 0, 0, 0, 0, 0, 0, 0, 0, 10]), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.hIndex([1, 1, 1, 1, 1, 1, 1, 1, 1, 1]), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.hIndex([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.hIndex([0, 0, 0, 0, 0, 0, 0, 0, 0, 1000]), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.hIndex([0, 0, 0, 0, 0, 0, 0, 0, 0, 9]), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.hIndex([0] * 99999 + [1000]), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
