"""
URL: https://leetcode.com/problems/sqrtx/description/

69. Sqrt(x)

Given a non-negative integer x, return the square root of x rounded down to the nearest integer. The returned integer should be non-negative as well.

You must not use any built-in exponent function or operator.

    For example, do not use pow(x, 0.5) in c++ or x ** 0.5 in python.


Example 1:

Input: x = 4
Output: 2

Example 2:

Input: x = 8
Output: 2
Explanation: The square root of 8 is 2.82842..., and since we round it down to the nearest integer, 2 is returned.


Constraints:

    0 <= x <= 2^31 - 1

"""


class Solution:
    def mySqrt(self, x: int) -> int:
        if x == 0:
            return 0
        low = 1
        high = x
        while low <= high:
            mid = low + (high - low) / 2
            res = int(mid * mid)
            if int(res) == x:
                return floor(mid)
            elif res < x:
                low = mid
            else:
                high = mid


sol = Solution()

# print(sol.mySqrt(4))  # 2

assert sol.mySqrt(4) == 2
assert sol.mySqrt(8) == 2
# assert sol.mySqrt(0) == 0
assert sol.mySqrt(1) == 1
assert sol.mySqrt(2) == 1
assert sol.mySqrt(3) == 1
assert sol.mySqrt(9) == 3
assert sol.mySqrt(16) == 4
assert sol.mySqrt(2147395600) == 46340
assert sol.mySqrt(2147483647) == 46340
assert sol.mySqrt(15) == 3
assert sol.mySqrt(17) == 4
assert sol.mySqrt(100000000) == 10000
assert sol.mySqrt(99999999) == 9999
