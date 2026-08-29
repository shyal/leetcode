"""
DRILL: Combinations
TRAINS: backtracking-start-index

Given two integers n and k, return every combination of k distinct
numbers drawn from 1 to n. Each combination lists its numbers in
increasing order. Two combinations that hold the same numbers are the
same combination, so return it once. The combinations may come back in
any order.

Example 1:

Input: n = 4, k = 2
Output: [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]
Explanation: [2, 1] is not listed. It holds the same numbers as [1, 2].

Example 2:

Input: n = 1, k = 1
Output: [[1]]

Example 3:

Input: n = 3, k = 3
Output: [[1, 2, 3]]
Explanation: k equals n, so there is one way to draw them all.

Constraints:

    1 <= n <= 20
    1 <= k <= n

    REQUIRED: [2, 1] is never built, not built and discarded. NO
    swapping elements of a list to control which numbers are still
    available, NO used or visited set, NO itertools, NO sorting or
    de-duplicating the answer at the end. Availability is decided on
    the way down, not repaired on the way out.
"""


class Solution:
    def combine(self, n: int, k: int) -> list[list[int]]:
        pass


sol = Solution()

print(sol.combine(4, 2))  # 6 pairs

# assert sorted(map(tuple, sol.combine(4, 2))) == [
#     (1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)
# ]
# assert sol.combine(1, 1) == [[1]]
# assert sol.combine(3, 3) == [[1, 2, 3]]
# assert sorted(map(tuple, sol.combine(3, 1))) == [(1,), (2,), (3,)]

# res = sol.combine(9, 3)
# assert len(res) == 84
# assert len({tuple(c) for c in res}) == 84
# assert all(len(c) == 3 and c == sorted(c) for c in res)

# res = sol.combine(20, 2)
# assert len(res) == 190
# assert all(1 <= a < b <= 20 for a, b in res)
