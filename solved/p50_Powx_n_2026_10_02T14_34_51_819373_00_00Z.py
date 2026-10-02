"""
URL: https://leetcode.com/problems/powx-n/description/?envType=problem-list-v2&envId=vn57k9wr

50. Pow(x, n)

Implement pow(x, n), which calculates x raised to the power n (i.e., x^n).

Example 1:

Input: x = 2.00000, n = 10
Output: 1024.00000

Example 2:

Input: x = 2.10000, n = 3
Output: 9.26100

Example 3:

Input: x = 2.00000, n = -2
Output: 0.25000
Explanation: 2^-2 = 1/2^2 = 1/4 = 0.25

Constraints:

    -100.0 < x < 100.0
    -2^31 <= n <= 2^31 - 1
    n is an integer.
    Either x is not zero or n > 0.
    -10^4 <= x^n <= 10^4
---
Very very vague idea.. the idea is, instead of performing n multiplications by n
we can perform fewer multiplications with a smaller value of n
e.g instead of doing

n = 4, x = 2
2 * 2 * 2 * 2
or 
4 * 4
if n = 10
2 * 2 * 2 * 2 * 2 * 2 * 2 * 2 * 2 * 2
becomes
4 * 4 * 4 * 4 * 4
becomes
16 * 16 * 4
becomes
256 * 4
solved positive numbers. just had negative numbers left, but got to attend to something
so dropping this for now.

LEETCODE: Time Limit Exceeded (2/309 cases)
"""


# mu 0.7
# def myPow(x: float, n: int) -> float
#   is_neg = n < 0
#   if n == 1
#     return x
#   if n == 2
#     return x * x
#   if even(n)
#     return self.myPow(x * x, n // 2)
#   else
#     return x * self.myPow(x * x, (n - 1) // 2)
#

def even(n):
    return n % 2 == 0


class Solution:
    def myPow(self, x: float, n: int) -> float:
        is_neg = n < 0
        if n == 1:
            return x
        if n == 2:
            return x * x
        if even(n):
            return self.myPow(x * x, n // 2)
        else:
            return x * self.myPow(x * x, (n - 1) // 2)


sol = Solution()
assert abs(sol.myPow(2.0, 10) - 1024.0) < 1e-05
assert abs(sol.myPow(2.1, 3) - 9.261) < 1e-05
