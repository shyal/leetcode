"""
Given three integers n, k and m, return the number of sequences of k
non-negative integers that have the sum n and whose first integer is m or
more. Two sequences with the same integers in a different order are
different sequences.

Example 1:

Input: n = 4, k = 3, m = 2
Output: 6
Explanation: The sequences are (2, 0, 2), (2, 1, 1), (2, 2, 0),
(3, 0, 1), (3, 1, 0) and (4, 0, 0).

Example 2:

Input: n = 3, k = 2, m = 5
Output: 0

Example 3:

Input: n = 5, k = 4, m = 5
Output: 1

Constraints:

    0 <= n, m <= 10^9
    1 <= k <= 10

    REQUIRED: O(k) time. NO enumeration of the sequences. NO recursion.
"""


class Solution:

    def sumsFrom(self, n: int, k: int, m: int) -> int:
        pass


sol = Solution()

print(sol.sumsFrom(4, 3, 2))  # 6

# assert sol.sumsFrom(4, 3, 2) == 6
# assert sol.sumsFrom(3, 2, 5) == 0
# assert sol.sumsFrom(5, 4, 5) == 1
# assert sol.sumsFrom(4, 3, 0) == 15
# assert sol.sumsFrom(4, 3, 1) == 10
# assert sol.sumsFrom(4, 3, 4) == 1
# assert sol.sumsFrom(4, 3, 5) == 0
# assert sol.sumsFrom(6, 1, 6) == 1
# assert sol.sumsFrom(6, 1, 2) == 1
# assert sol.sumsFrom(20, 6, 9) == 4368
# assert sol.sumsFrom(0, 3, 0) == 1
# assert sol.sumsFrom(10**9, 2, 10**9 - 4) == 5
