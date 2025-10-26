"""
URL: https://leetcode.com/problems/sum-of-digits-in-base-k/description/?envType=problem-list-v2&envId=vn57k9wr

1837. Sum of Digits in Base K

Given an integer n (in base 10) and a base k, return the sum of the digits of n after converting n from base 10 to base k.

After converting, each digit should be interpreted as a base 10 number, and the sum should be returned in base 10.

Example 1:

Input: n = 34, k = 6
Output: 9
Explanation: 34 (base 10) expressed in base 6 is 54. 5 + 4 = 9.

Example 2:

Input: n = 10, k = 10
Output: 1
Explanation: n is already in base 10. 1 + 0 = 1.

Constraints:

    1 <= n <= 100
    2 <= k <= 10

---

Base conversion is one of those things that easily slips my mind.

Let's go through some base conversions by hand:

10 in binary as base 10:

1           0
2^1 * 1     2^0 * 0


The above method involves working directly with the digits.

However we can also use divmod, e.g going from 10 base 10 to binary:

>>> divmod(10, 2)
(5, 0)
>>> divmod(5, 2)
(2, 1)
>>> divmod(2, 2)
(1, 0)
>>> divmod(1, 2)
(0, 1)

The output being 0101.

So we recursively run divmod on the number until we get 0, and the remainder
forms the digits of the new base.

"""


class Solution:
    def toBase(self, n, k):
        res = []
        while n:
            n, m = divmod(n, k)
            res = [m] + res
        return reduce(lambda acc, val: acc * 10 + val, res)

    def getDigits(self, num):
        digits = []
        while num:
            digits.append(num % 10)
            num //= 10
        return digits

    def sumBase(self, n: int, k: int) -> int:
        n = self.toBase(n, k)
        digits = self.getDigits(n)
        return sum(digits)


sol = Solution()


assert sol.sumBase(34, 6) == 9
assert sol.sumBase(10, 10) == 1
assert sol.sumBase(1, 2) == 1
assert sol.sumBase(1, 10) == 1
assert sol.sumBase(100, 10) == 1
assert sol.sumBase(100, 2) == 3
assert sol.sumBase(99, 10) == 18
assert sol.sumBase(2, 2) == 1
assert sol.sumBase(3, 2) == 2
assert sol.sumBase(7, 8) == 7
assert sol.sumBase(8, 8) == 1
assert sol.sumBase(9, 10) == 9
assert sol.sumBase(13, 3) == 3
assert sol.sumBase(27, 3) == 1
assert sol.sumBase(100, 9) == 4
