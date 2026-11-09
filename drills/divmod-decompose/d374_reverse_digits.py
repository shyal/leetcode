"""
EPI 4.8 Reverse digits

Given an integer x, return the integer whose decimal digits are the
digits of x in reverse order, with the sign of x.

Example 1:

Input: x = 42
Output: 24

Example 2:

Input: x = -314
Output: -413

Example 3:

Input: x = 1200
Output: 21
Explanation: the reverse is 0021, and the leading zeros are not part of
the number.

Constraints:

    -2^63 <= x < 2^63

    REQUIRED: O(n) time, where n is the number of digits of x. NO str(),
    NO repr(), NO f-string, NO format().
"""


class Solution:
    def reverse(self, x: int) -> int:
        pass


sol = Solution()

print(sol.reverse(42))  # 24

# assert sol.reverse(42) == 24
# assert sol.reverse(-314) == -413
# assert sol.reverse(1200) == 21
# assert sol.reverse(0) == 0
# assert sol.reverse(7) == 7
# assert sol.reverse(-7) == -7
# assert sol.reverse(10) == 1
# assert sol.reverse(-10) == -1
# assert sol.reverse(1001) == 1001
# assert sol.reverse(123456789) == 987654321
# assert sol.reverse(2 ** 63 - 1) == 7085774586302733229
# assert sol.reverse(-2 ** 63) == -8085774586302733229
# assert sol.reverse(1000000000000000000) == 1
# assert sol.reverse(-9000000000000000009) == -9000000000000000009
