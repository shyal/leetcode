"""
DRILL: Triples
TRAINS: backtracking-start-index

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


class Solution:
    def triples(self, n: int) -> list[list[int]]:
        ret = []
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    ret.append([i, j, k])
        return ret


sol = Solution()

print(
    sol.triples(5)
)  # [[0, 1, 2], [0, 1, 3], [0, 1, 4], [0, 2, 3], [0, 2, 4], [0, 3, 4], [1, 2, 3], [1, 2, 4], [1, 3, 4], [2, 3, 4]]

assert sol.triples(5) == [
    [0, 1, 2],
    [0, 1, 3],
    [0, 1, 4],
    [0, 2, 3],
    [0, 2, 4],
    [0, 3, 4],
    [1, 2, 3],
    [1, 2, 4],
    [1, 3, 4],
    [2, 3, 4],
]
assert sol.triples(2) == []
assert sol.triples(3) == [[0, 1, 2]]

res = sol.triples(30)
assert len(res) == 4060 and len({tuple(t) for t in res}) == 4060
assert all(0 <= a < b < c < 30 for a, b, c in res)
