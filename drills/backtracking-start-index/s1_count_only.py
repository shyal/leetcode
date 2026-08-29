"""
DRILL: Count Only
TRAINS: backtracking-start-index

Given two integers n and k, return how many combinations of k distinct
numbers can be drawn from 1 to n. Two combinations that hold the same
numbers are the same combination, so count it once.

Example 1:

Input: n = 4, k = 2
Output: 6
Explanation: the combinations are [1, 2], [1, 3], [1, 4], [2, 3],
[2, 4] and [3, 4].

Example 2:

Input: n = 5, k = 3
Output: 10

Example 3:

Input: n = 3, k = 3
Output: 1
Explanation: k equals n, so there is one way to draw them all.

Constraints:

    1 <= n <= 16
    1 <= k <= n

    REQUIRED: the count comes from visiting every combination once and
    never visiting the same one twice; k is an argument, so the depth is
    not known when the code is written. NO math.comb, NO factorial
    formula, NO Pascal table, NO itertools, NO list of chosen numbers -
    nothing is appended or popped anywhere in the solution.
"""


class Solution:
    def count(self, n: int, k: int) -> int:
        pass


sol = Solution()

print(sol.count(4, 2))  # 6

# assert sol.count(4, 2) == 6
# assert sol.count(5, 3) == 10
# assert sol.count(3, 3) == 1
# assert sol.count(1, 1) == 1
# assert sol.count(6, 1) == 6

# from math import comb
# for n in range(1, 13):
#     for k in range(1, n + 1):
#         assert sol.count(n, k) == comb(n, k), (n, k)

# assert sol.count(16, 8) == 12870
