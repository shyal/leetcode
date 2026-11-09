"""
EPI 4.7 Compute pow(x,y)

Given a float x and an integer y, return x raised to the power y.

Example 1:

Input: x = 2.0, y = 10
Output: 1024.0

Example 2:

Input: x = 2.0, y = -2
Output: 0.25
Explanation: 2.0 to the power -2 is 1 / 4.

Example 3:

Input: x = -1.5, y = 3
Output: -3.375

Constraints:

    -100.0 <= x <= 100.0
    -2^31 <= y < 2^31
    x != 0 when y < 0
    The result fits in a float.

    REQUIRED: O(log |y|) multiplications. NO **, NO pow(), NO
    math.pow(), NO math.exp().
"""


class Solution:
    def power(self, x: float, y: int) -> float:
        pass


sol = Solution()

print(sol.power(2.0, 10))  # 1024.0

# assert sol.power(2.0, 10) == 1024.0
# assert sol.power(2.0, -2) == 0.25
# assert sol.power(-1.5, 3) == -3.375
# assert sol.power(5.0, 0) == 1.0
# assert sol.power(0.0, 0) == 1.0
# assert sol.power(0.0, 5) == 0.0
# assert sol.power(7.0, 1) == 7.0
# assert sol.power(-2.0, 2) == 4.0
# assert sol.power(3.0, 30) == 205891132094649.0
# assert sol.power(2.0, 1000) == 2.0 ** 1000
# assert sol.power(2.0, -1000) == 2.0 ** -1000
# assert isclose(sol.power(10.0, -3), 0.001, rel_tol=1e-12)
# assert sol.power(1.0, 2 ** 31 - 1) == 1.0
# assert sol.power(-1.0, 2 ** 31 - 1) == -1.0
# assert sol.power(-1.0, -2 ** 31) == 1.0
# assert isclose(sol.power(1.0000001, 10 ** 9), 1.0000001 ** 10 ** 9, rel_tol=1e-6)
