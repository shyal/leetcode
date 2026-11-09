"""
EPI 11.5 Compute the real square root

Given a positive float x, return its square root within a relative
error of 10^-9: the result r satisfies |r - s| <= 10^-9 * s, where s is
the exact square root of x.

Example 1:

Input: x = 2.0
Output: 1.414213562...

Example 2:

Input: x = 0.25
Output: 0.5
Explanation: the square root is larger than x when x < 1.

Example 3:

Input: x = 1.0
Output: 1.0

Constraints:

    10^-6 <= x <= 10^9

    REQUIRED: O(log(x / 10^-9)) time, O(1) extra space. NO math.sqrt,
    NO math.pow, NO ** with a fractional exponent, NO math.log, NO
    math.exp, NO Newton's method.
"""


class Solution:
    def square_root(self, x: float) -> float:
        pass


sol = Solution()

print(sol.square_root(2.0))  # 1.414213562...


def close(x):
    return isclose(sol.square_root(x), x ** 0.5, rel_tol=1e-9)


# assert close(2.0)
# assert close(0.25)
# assert close(1.0)
# assert close(4.0)
# assert close(9.0)
# assert close(3.0)
# assert close(0.5)
# assert close(0.01)
# assert close(0.999999)
# assert close(1.000001)
# assert close(1e-6)
# assert close(1.5e-6)
# assert close(123456.789)
# assert close(1e9)
# assert close(999999999.5)
# assert close(31622.0)
