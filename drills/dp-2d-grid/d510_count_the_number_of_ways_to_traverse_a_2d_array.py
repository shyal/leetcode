"""
EPI 16.3 Count the number of ways to traverse a 2D array

Given n and m, return the number of paths from the top-left cell to the
bottom-right cell of a grid with n rows and m columns, where each step
moves one cell right or one cell down.

Example 1:

Input: n = 3, m = 3
Output: 6
Explanation: each path is 2 steps right and 2 steps down, in some order.

    S . .
    . . .
    . . E

Example 2:

Input: n = 2, m = 3
Output: 3
Explanation: RRD, RDR and DRR.

Example 3:

Input: n = 1, m = 1
Output: 1
Explanation: the path with no steps.

Constraints:

    1 <= n, m <= 100

    REQUIRED: O(n * m) time and O(min(n, m)) extra space. NO
    math.comb. NO factorial.
"""


class Solution:
    def number_of_ways(self, n: int, m: int) -> int:
        pass


sol = Solution()

print(sol.number_of_ways(3, 3))  # 6

# assert sol.number_of_ways(3, 3) == 6
# assert sol.number_of_ways(2, 3) == 3
# assert sol.number_of_ways(1, 1) == 1
# assert sol.number_of_ways(2, 2) == 2
# assert sol.number_of_ways(5, 5) == 70
# assert sol.number_of_ways(3, 7) == 28
# assert sol.number_of_ways(7, 3) == 28
# assert sol.number_of_ways(1, 100) == 1
# assert sol.number_of_ways(100, 1) == 1
# assert sol.number_of_ways(16, 16) == 155117520
# assert sol.number_of_ways(100, 100) == 22750883079422934966181954039568885395604168260154104734000
