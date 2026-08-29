"""
DRILL: Pairs
TRAINS: backtracking-start-index

Given an integer n, return every pair [a, b] of distinct numbers drawn
from 1 to n, with a < b. Two pairs that hold the same numbers are the
same pair, so return it once. The pairs may come back in any order.

Example 1:

Input: n = 3
Output: [[1, 2], [1, 3], [2, 3]]
Explanation: [2, 1] is not listed. It holds the same numbers as [1, 2].

Example 2:

Input: n = 1
Output: []
Explanation: there is only one number to draw from.

Constraints:

    1 <= n <= 30

    REQUIRED: [2, 1] is never built, not built and discarded. NO
    recursion, NO itertools, NO filtering a pair after it is built, NO
    set or de-duplication of the answer. Which numbers are still
    available is settled before the next number is chosen.
"""


class Solution:
    def pairs(self, n: int) -> list[list[int]]:
        pass


sol = Solution()

print(sol.pairs(3))  # 3 pairs

# assert sorted(map(tuple, sol.pairs(3))) == [(1, 2), (1, 3), (2, 3)]
# assert sol.pairs(1) == []
# assert sol.pairs(2) == [[1, 2]]

# res = sol.pairs(30)
# assert len(res) == 435 and len({tuple(p) for p in res}) == 435
# assert all(1 <= a < b <= 30 for a, b in res)
