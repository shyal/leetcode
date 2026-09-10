"""
URL: https://leetcode.com/problems/sqrtx/description/?envType=problem-list-v2&envId=vn57k9wr

69. Sqrt(x)

Given a non-negative integer x, return the square root of x rounded down to the nearest integer. The returned integer should be non-negative as well.

You must not use any built-in exponent function or operator.

For example, do not use pow(x, 0.5) in c++ or x ** 0.5 in python.

Example 1:

Input: x = 4
Output: 2
Explanation: The square root of 4 is 2, so we return 2.

Example 2:

Input: x = 8
Output: 2
Explanation: The square root of 8 is 2.82842..., and since we round it down to the nearest integer, 2 is returned.

Constraints:

    0 <= x <= 2^31 - 1

---

Hint: returned mid instead of right

"""


class Solution:
    def mySqrt(self, x: int) -> int:
        left, right = 0, x
        while left <= right:
            mid = (left + right) // 2
            res = mid * mid
            if res == x:
                return mid
            elif res > x:
                right = mid - 1
            else:
                left = mid + 1
        return right


sol = Solution()

print(sol.mySqrt(4))  # 2
print(sol.mySqrt(8))  # 2

assert sol.mySqrt(4) == 2
assert sol.mySqrt(8) == 2

assert sol.mySqrt(0) == 0
assert sol.mySqrt(1) == 1
assert sol.mySqrt(2) == 1
assert sol.mySqrt(3) == 1
assert sol.mySqrt(15) == 3
assert sol.mySqrt(16) == 4
assert sol.mySqrt(17) == 4
assert sol.mySqrt(2147395599) == 46339
assert sol.mySqrt(2147483647) == 46340
assert sol.mySqrt(1000000) == 1000
assert sol.mySqrt(999999) == 999
assert sol.mySqrt(25) == 5
