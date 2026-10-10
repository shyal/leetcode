"""
URL: https://leetcode.com/problems/merge-triplets-to-form-target-triplet/description/?envType=problem-list-v2&envId=vn57k9wr

1899. Merge Triplets to Form Target Triplet

A triplet is an array of three integers. You are given a 2D integer array triplets, where triplets[i] = [a_i, b_i, c_i] describes the iᵗʰ triplet. You are also given an integer array target = [x, y, z] that describes the triplet you want to obtain.

To obtain target, you may apply the following operation on triplets any number of times (possibly zero):

- Choose two indices (0-indexed) i and j (i != j) and update triplets[j] to become [max(a_i, a_j), max(b_i, b_j), max(c_i, c_j)].

For example, if triplets[i] = [2, 5, 3] and triplets[j] = [1, 7, 5], triplets[j] will be updated to [max(2, 1), max(5, 7), max(3, 5)] = [2, 7, 5].

Return true if it is possible to obtain the target triplet [x, y, z] as an element of triplets, or false otherwise.

Example 1:

Input: triplets = [[2,5,3],[1,8,4],[1,7,5]], target = [2,7,5]
Output: true
Explanation:
Perform the following operations:
- Choose the first and last triplets [[2,5,3],[1,8,4],[1,7,5]]. Update the last triplet to be [max(2,1), max(5,7), max(3,5)] = [2,7,5]. triplets = [[2,5,3],[1,8,4],[2,7,5]]
The target triplet [2,7,5] is now an element of triplets.

Example 2:

Input: triplets = [[3,4,5],[4,5,6]], target = [3,2,5]
Output: false
Explanation:
It is impossible to have [3,2,5] as an element because there is no 2 in any of the triplets.

Example 3:

Input: triplets = [[2,5,3],[2,3,4],[1,2,5],[5,2,3]], target = [5,5,5]
Output: true
Explanation:
Perform the following operations:
- Choose the first and third triplets [[2,5,3],[2,3,4],[1,2,5],[5,2,3]]. Update the third triplet to be [max(2,1), max(5,2), max(3,5)] = [2,5,5]. triplets = [[2,5,3],[2,3,4],[2,5,5],[5,2,3]].
- Choose the third and fourth triplets [[2,5,3],[2,3,4],[2,5,5],[5,2,3]]. Update the fourth triplet to be [max(2,5), max(5,2), max(5,3)] = [5,5,5]. triplets = [[2,5,3],[2,3,4],[2,5,5],[5,5,5]].
The target triplet [5,5,5] is now an element of triplets.

Constraints:

    1 <= triplets.length <= 10^5
    triplets[i].length == target.length == 3
    1 <= a_i, b_i, c_i, x, y, z <= 1000
---
if a number in target is in any of the triplets (in the right column) then
we're likely to be able to form the target from the triplets as long as one of the
other numbers in that triplet maxes out other numbers.
in other words, 

e.g with [[3, 5, 1], [10, 5, 7]] [3, 5, 7] we have a problem, we cannot use 10, 5, 7.
the analytical / greedy approach is quite tough to work out, actually, so maybe
a BFS would get us there? 

Let's not give up on the analytical / greedy approach.


[2, 5, 3], [1, 8, 4], [1, 7, 5]], [2, 7, 5]

Look for triplets with 2 in col 0: [2, 5, 3] we can use it, because it doesn't contain
a number greater than the other columns in target

Look for a triplet with 7 in col 1: [1, 7, 5], ditto

Look for a triplet with 5 in col 1: [1, 7, 5], ditto
so it really makes sense sorting the triplets

LEETCODE: Accepted (30 ms, 54.1 MB)
"""


# mu 0.7
# def mergeTriplets(triplets: [[int]], target: [int]) -> bool
#   res = [False, False, False]
#   for (a, b, c) in triplets
#     if a == target[0] and b <= target[1] and c <= target[2]
#       res[0] = True
#     if a <= target[0] and b == target[1] and c <= target[2]
#       res[1] = True
#     if a <= target[0] and b <= target[1] and c == target[2]
#       res[2] = True
#   all res

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
    def mergeTriplets(self, triplets: list[list[int]], target: list[int]) -> bool:
        _in_triplets, triplets = triplets, Grid(triplets)
        _w_triplets = triplets
        try:
            res = [False, False, False]
            for (a, b, c) in triplets:
                if a == target[0] and b <= target[1] and c <= target[2]:
                    res[0] = True
                if a <= target[0] and b == target[1] and c <= target[2]:
                    res[1] = True
                if a <= target[0] and b <= target[1] and c == target[2]:
                    res[2] = True
            return all(res)
        finally:
            _in_triplets[:] = _w_triplets


sol = Solution()
print(sol.mergeTriplets([[3, 5, 1], [10, 5, 7]], [3, 5, 7]))
print(sol.mergeTriplets([[2, 5, 3], [1, 8, 4], [1, 7, 5]], [2, 7, 5]))
_l, _r = sol.mergeTriplets([[2, 5, 3], [1, 8, 4], [1, 7, 5]], [2, 7, 5]), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.mergeTriplets([[3, 4, 5], [4, 5, 6]], [3, 2, 5]), False
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.mergeTriplets([[2, 5, 3], [2, 3, 4], [1, 2, 5], [5, 2, 3]], [5, 5, 5]), True
assert _l is _r, f"left : {_l!r}\nright: {_r!r}\nop   : is"
_l, _r = sol.mergeTriplets([[1, 1, 1]], [1, 1, 1]), True
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.mergeTriplets([[1000, 1000, 1000]], [1000, 1000, 1000]), True
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.mergeTriplets([[1, 2, 3], [3, 2, 1], [2, 3, 1]], [3, 3, 3]), True
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.mergeTriplets([[1, 1, 1], [1, 1, 1], [1, 1, 1]], [1, 1, 1]), True
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.mergeTriplets([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [7, 8, 9]), True
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.mergeTriplets([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [10, 10, 10]), False
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.mergeTriplets([[2, 2, 2], [2, 2, 2], [2, 2, 2]], [2, 2, 2]), True
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.mergeTriplets([[1, 1000, 1], [1000, 1, 1], [1, 1, 1000]], [1000, 1000, 1000]), True
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.mergeTriplets([[1, 2, 3], [3, 2, 1], [2, 3, 1], [3, 3, 3]], [3, 3, 3]), True
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.mergeTriplets([[1, 2, 3], [3, 2, 1], [2, 3, 1]], [3, 3, 2]), False
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.mergeTriplets([[1000, 999, 998], [997, 996, 995], [994, 993, 992]], [1000, 999, 998]), True
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.mergeTriplets([[1, 1, 1]], [2, 2, 2]), False
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
