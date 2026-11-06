"""
Given a nonnegative number x and a positive integer n, return the
positive n'th root of x within an error of 0.001: the real root y
satisfies |y - root(x, n)| < 0.001.

Example 1:

Input: x = 7, n = 3
Output: 1.913
Explanation: the real root is 1.91293... Any value within 0.001 of it
is accepted.

Example 2:

Input: x = 0.25, n = 2
Output: 0.5
Explanation: the root is larger than x when x < 1.

Example 3:

Input: x = 9, n = 2
Output: 3

Constraints:

    0 <= x <= 10^9
    1 <= n <= 30

    REQUIRED: O(log(x / 0.001)) time. NO ** with a fractional exponent,
    NO math.pow, NO math.log, NO Newton's method.
"""


class Solution:
    def root(self, x: float, n: int) -> float:
        pass


sol = Solution()

print(sol.root(7, 3))  # 1.913

# assert abs(sol.root(7, 3) - 7 ** (1 / 3)) < 0.001
# assert abs(sol.root(0.25, 2) - 0.5) < 0.001
# assert abs(sol.root(9, 2) - 3) < 0.001
# assert abs(sol.root(4, 2) - 2) < 0.001
# assert abs(sol.root(27, 3) - 3) < 0.001
# assert abs(sol.root(16, 4) - 2) < 0.001
# assert abs(sol.root(3, 2) - 3 ** 0.5) < 0.001
# assert abs(sol.root(10, 3) - 10 ** (1 / 3)) < 0.001
# assert abs(sol.root(160, 3) - 160 ** (1 / 3)) < 0.001
# assert abs(sol.root(0, 2) - 0) < 0.001
# assert abs(sol.root(0, 7) - 0) < 0.001
# assert abs(sol.root(1, 1) - 1) < 0.001
# assert abs(sol.root(1, 30) - 1) < 0.001
# assert abs(sol.root(5, 1) - 5) < 0.001
# assert abs(sol.root(0.5, 3) - 0.5 ** (1 / 3)) < 0.001
# assert abs(sol.root(0.001, 2) - 0.001 ** 0.5) < 0.001
# assert abs(sol.root(10 ** 9, 2) - 31622.7766) < 0.001
# assert abs(sol.root(10 ** 9, 3) - 1000) < 0.001
# assert abs(sol.root(10 ** 9, 30) - (10 ** 9) ** (1 / 30)) < 0.001
# assert abs(sol.root(2, 30) - 2 ** (1 / 30)) < 0.001
