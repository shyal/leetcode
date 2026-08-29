"""
DRILL: Triples
TRAINS: backtracking-start-index

Given an integer n, return every triple [a, b, c] of distinct numbers
drawn from 1 to n, with a < b < c. Two triples that hold the same
numbers are the same triple, so return it once. The triples may come
back in any order.

Example 1:

Input: n = 4
Output: [[1, 2, 3], [1, 2, 4], [1, 3, 4], [2, 3, 4]]
Explanation: [2, 1, 3] is not listed. It holds the same numbers as
[1, 2, 3].

Example 2:

Input: n = 2
Output: []
Explanation: there are only two numbers to draw from.

Constraints:

    1 <= n <= 30

    REQUIRED: [2, 1, 3] is never built, not built and discarded. NO
    recursion, NO itertools, NO filtering a triple after it is built,
    NO set or de-duplication of the answer. Which numbers are still
    available is settled before the next number is chosen.
"""


class Solution:
    def triples(self, n: int) -> list[list[int]]:
        pass


sol = Solution()

print(sol.triples(4))  # 4 triples

# assert sorted(map(tuple, sol.triples(4))) == [
#     (1, 2, 3), (1, 2, 4), (1, 3, 4), (2, 3, 4)
# ]
# assert sol.triples(2) == []
# assert sol.triples(3) == [[1, 2, 3]]

# res = sol.triples(10)
# assert len(res) == 120 and len({tuple(t) for t in res}) == 120
# assert all(1 <= a < b < c <= 10 for a, b, c in res)

# res = sol.triples(30)
# assert len(res) == 4060 and len({tuple(t) for t in res}) == 4060
