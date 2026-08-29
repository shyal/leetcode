"""
DRILL: Pairs Then Triples
TRAINS: backtracking-start-index

Given an integer n, return every pair [a, b] of distinct numbers drawn
from 1 to n, with a < b. Then, in a second method, return every triple
[a, b, c] of distinct numbers drawn from 1 to n, with a < b < c. Two
pairs that hold the same numbers are the same pair, so return it once;
the same holds for triples. The pairs and triples may come back in any
order.

Example 1:

Input: n = 3
Output (pairs): [[1, 2], [1, 3], [2, 3]]
Explanation: [2, 1] is not listed. It holds the same numbers as [1, 2].

Example 2:

Input: n = 4
Output (triples): [[1, 2, 3], [1, 2, 4], [1, 3, 4], [2, 3, 4]]

Example 3:

Input: n = 2
Output (triples): []
Explanation: there are only two numbers to draw from.

Constraints:

    1 <= n <= 30

    REQUIRED: [2, 1] is never built, not built and discarded. NO
    recursion, NO itertools, NO filtering a pair or triple after it is
    built, NO set or de-duplication of the answer. Which numbers are
    still available is settled before the next number is chosen.
"""


class Solution:
    def pairs(self, n: int) -> list[list[int]]:
        pass

    def triples(self, n: int) -> list[list[int]]:
        pass


sol = Solution()

print(sol.pairs(3))  # 3 pairs
print(sol.triples(4))  # 4 triples

# assert sorted(map(tuple, sol.pairs(3))) == [(1, 2), (1, 3), (2, 3)]
# assert sol.pairs(1) == []
# assert sol.pairs(2) == [[1, 2]]

# assert sorted(map(tuple, sol.triples(4))) == [
#     (1, 2, 3), (1, 2, 4), (1, 3, 4), (2, 3, 4)
# ]
# assert sol.triples(2) == []
# assert sol.triples(3) == [[1, 2, 3]]

# res = sol.pairs(30)
# assert len(res) == 435 and len({tuple(p) for p in res}) == 435
# assert all(1 <= a < b <= 30 for a, b in res)

# res = sol.triples(10)
# assert len(res) == 120 and len({tuple(t) for t in res}) == 120
# assert all(1 <= a < b < c <= 10 for a, b, c in res)
