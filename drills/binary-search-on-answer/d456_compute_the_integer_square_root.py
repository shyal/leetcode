"""
EPI 11.4 Compute the integer square root

Given a nonnegative integer k, return the largest integer whose square
is less than or equal to k.

Example 1:

Input: k = 300
Output: 17
Explanation: 17 * 17 = 289 <= 300 and 18 * 18 = 324 > 300.

Example 2:

Input: k = 16
Output: 4

Example 3:

Input: k = 0
Output: 0

Constraints:

    0 <= k <= 10^18

    REQUIRED: O(log k) time, O(1) extra space. NO math.sqrt, NO
    math.isqrt, NO ** with a fractional exponent, NO floats, NO
    Newton's method.
"""


class Solution:
    def square_root(self, k: int) -> int:
        pass


sol = Solution()

print(sol.square_root(300))  # 17

# assert sol.square_root(300) == 17
# assert sol.square_root(16) == 4
# assert sol.square_root(0) == 0
# assert sol.square_root(1) == 1
# assert sol.square_root(2) == 1
# assert sol.square_root(3) == 1
# assert sol.square_root(4) == 2
# assert sol.square_root(8) == 2
# assert sol.square_root(9) == 3
# assert sol.square_root(15) == 3
# assert sol.square_root(24) == 4
# assert sol.square_root(25) == 5
# assert sol.square_root(2 ** 31 - 1) == 46340
# assert sol.square_root(10 ** 18) == 10 ** 9
# assert sol.square_root(10 ** 18 - 1) == 10 ** 9 - 1
# assert sol.square_root(999999999999999999 // 7) == 377964473
