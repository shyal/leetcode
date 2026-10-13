"""
DRILL: Triples

Given an integer n, return every triple [a, b, c] of integers with
0 <= a < b < c < n. List the triples in lexicographic order.

Example 1:

Input: n = 5
Output: [[0, 1, 2], [0, 1, 3], [0, 1, 4], [0, 2, 3], [0, 2, 4], [0, 3, 4],
[1, 2, 3], [1, 2, 4], [1, 3, 4], [2, 3, 4]]

Example 2:

Input: n = 2
Output: []
Explanation: Only 0 and 1 are available, and a triple needs three integers.

Constraints:

    1 <= n <= 30

    REQUIRED: NO recursion.

"""


# mu 0.10
# class Solution
#   def triples(n: int) -> [[int]]
#     [list(x) for x in triples(n)]

def triples(n, type=tuple):
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                yield type((i, j, k))


class Solution:
    def triples(self, n: int) -> list[list[int]]:
        return [list(x) for x in triples(n)]


sol = Solution()
print(sol.triples(5))
_l, _r = sol.triples(5), [[0, 1, 2], [0, 1, 3], [0, 1, 4], [0, 2, 3], [0, 2, 4], [0, 3, 4], [1, 2, 3], [1, 2, 4], [1, 3, 4], [2, 3, 4]]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.triples(2), []
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.triples(3), [[0, 1, 2]]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
res = sol.triples(30)
assert len(res) == 4060 and len({tuple(t) for t in res}) == 4060
assert all((0 <= a < b < c < 30 for a, b, c in res))
