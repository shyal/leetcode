"""
EPI 4.5 Compute product without arithmetical operators

Given two nonnegative integers x and y, return their product. The only
operators you may use are assignment, the bitwise operators >>, <<, |,
&, ~ and ^, and the equality tests == and !=.

Example 1:

Input: x = 5, y = 6
Output: 30

Example 2:

Input: x = 0, y = 7
Output: 0

Example 3:

Input: x = 13, y = 1
Output: 13

Constraints:

    0 <= x < 2^32
    0 <= y < 2^32

    REQUIRED: O(n^2) time, where n is the number of bits in x and y.
    NO +, -, *, /, //, %, ** and NO augmented form of them (+= and so
    on). NO <, <=, >, >=. NO sum(), NO range().
"""


class Solution:
    def multiply(self, x: int, y: int) -> int:
        pass


sol = Solution()

print(sol.multiply(5, 6))  # 30

# assert sol.multiply(5, 6) == 30
# assert sol.multiply(0, 7) == 0
# assert sol.multiply(7, 0) == 0
# assert sol.multiply(0, 0) == 0
# assert sol.multiply(13, 1) == 13
# assert sol.multiply(1, 13) == 13
# assert sol.multiply(2, 2) == 4
# assert sol.multiply(255, 255) == 65025
# assert sol.multiply(1 << 31, 2) == 1 << 32
# assert sol.multiply(2 ** 32 - 1, 2 ** 32 - 1) == 18446744065119617025
# assert sol.multiply(123456789, 987654321) == 121932631112635269
# assert sol.multiply(65536, 65536) == 4294967296
# assert all(sol.multiply(a, b) == a * b for a in range(40) for b in range(40))
