"""
DRILL: Combinations
TRAINS: backtracking-start-index

Given two integers n and k, return every combination of k distinct
numbers drawn from 1 to n. Each combination lists its numbers in
increasing order.

Example 1:

Input: n = 4, k = 2
Output: [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]

Example 2:

Input: n = 3, k = 3
Output: [[1, 2, 3]]

Constraints:

    1 <= n <= 20
    1 <= k <= n

REQUIRED: [2, 1] is never built, not built and discarded. NO swapping
elements of a list, NO used or visited set, NO itertools, NO sorting or
de-duplicating the answer at the end.

"""


class Solution:
    def combine(self, n: int, k: int) -> list[list[int]]:
        pass


sol = Solution()

print(sol.combine(4, 2))

# assert sol.combine(4, 2) == [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]
# assert sol.combine(1, 1) == [[1]]
# assert sol.combine(3, 3) == [[1, 2, 3]]
# assert sol.combine(3, 1) == [[1], [2], [3]]

# res = sol.combine(9, 3)
# assert len(res) == 84
# assert len({tuple(c) for c in res}) == 84
# assert all(len(c) == 3 and c == sorted(c) for c in res)

# res = sol.combine(20, 2)
# assert len(res) == 190
# assert all(1 <= a < b <= 20 for a, b in res)
