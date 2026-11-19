"""
Given two integers n and k, return the number of sequences of k
non-negative integers that have the sum n. Two sequences with the same
integers in a different order are different sequences.

Example 1:

Input: n = 2, k = 3
Output: 6
Explanation: The sequences are (2, 0, 0), (0, 2, 0), (0, 0, 2),
(1, 1, 0), (1, 0, 1) and (0, 1, 1).

Example 2:

Input: n = 4, k = 2
Output: 5
Explanation: The sequences are (0, 4), (1, 3), (2, 2), (3, 1) and (4, 0).

Example 3:

Input: n = 0, k = 5
Output: 1

Use the stars and bars formula.

Constraints:

    0 <= n <= 10^9
    1 <= k <= 10

    REQUIRED: O(k) time. NO enumeration of the sequences. NO recursion.
"""


class Solution:

    def sums(self, n: int, k: int) -> int:
        pass


sol = Solution()

print(sol.sums(2, 3))  # 6

# assert sol.sums(2, 3) == 6
# assert sol.sums(4, 2) == 5
# assert sol.sums(0, 5) == 1
# assert sol.sums(7, 1) == 1
# assert sol.sums(0, 1) == 1
# assert sol.sums(1, 4) == 4
# assert sol.sums(4, 3) == 15
# assert sol.sums(5, 4) == 56
# assert sol.sums(20, 6) == 53130
# assert sol.sums(10**9, 2) == 10**9 + 1
# assert sol.sums(10**6, 3) == 500001500001
