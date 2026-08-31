"""
DRILL: Pairs
TRAINS: backtracking-start-index

Given an integer n, return every pair [a, b] of integers with
0 <= a < b < n. List the pairs in lexicographic order.

Example 1:

Input: n = 4
Output: [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]]

Example 2:

Input: n = 1
Output: []
Explanation: Only 0 is available, and a pair needs two integers.

Constraints:

    1 <= n <= 30

    REQUIRED: NO recursion.

"""


class Solution:
    def pairs(self, n: int) -> list[list[int]]:
        pass


sol = Solution()

print(sol.pairs(4))  # [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]]

# assert sol.pairs(4) == [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]]
# assert sol.pairs(1) == []
# assert sol.pairs(2) == [[0, 1]]

# res = sol.pairs(30)
# assert len(res) == 435 and len({tuple(p) for p in res}) == 435
# assert all(0 <= a < b < 30 for a, b in res)
