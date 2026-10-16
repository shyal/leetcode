"""
URL: https://leetcode.com/problems/factorial-trailing-zeroes/description/?envType=problem-list-v2&envId=vn57k9wr

172. Factorial Trailing Zeroes

Given an integer n, return the number of trailing zeroes in n!.

Note that n! = n * (n - 1) * (n - 2) * ... * 3 * 2 * 1.

Example 1:

Input: n = 3
Output: 0
Explanation: 3! = 6, no trailing zero.

Example 2:

Input: n = 5
Output: 1
Explanation: 5! = 120, one trailing zero.

Example 3:

Input: n = 0
Output: 0

Constraints:

    0 <= n <= 10^4

Follow up:
Could you write a solution that works in logarithmic time complexity?

---

LEETCODE: Accepted (6747 ms, 34.2 MB)
"""


# mu 0.12
# class Solution
#   def trailingZeroes(n: int) -> int
#     def factorial(n)
#       ret res = 1
#       while n
#         res *= n
#         n -= 1
#     ret count = 0
#     for d in to_digits(factorial(n))[::-1]
#       if d == 0
#         count += 1
#       else
#         break

def to_digits(num, reverse=False, base=10):
    if isinstance(num, str):
        ds = [int(c, base) for c in num.lstrip('-')]
    else:
        num = abs(num)
        ds = []
        while True:
            (num, d) = divmod(num, base)
            ds.append(d)
            if num == 0:
                break
        ds.reverse()
    return ds[::-1] if reverse else ds


# mu 0.12
# import math
#
# class Solution
#   def trailingZeroes(n: int) -> int
#     def factorial(n)
#       ret res = 1
#       while n
#         res *= n
#         n -= 1
#     fact = factorial(n)
#     num_digits = ceil(math.log(fact, 10))
#     return first_true(0, num_digits, x -> fact != (fact // 10**x) * 10**x) - 1

from bisect import bisect_left
from math import ceil
import math


def first_true(lo, hi, ok):
    return lo + bisect_left(range(lo, hi + 1), True, key=ok)


class Solution:
    def trailingZeroes(self, n: int) -> int:
        def factorial(n):
            res = 1
            while n:
                res *= n
                n -= 1
            return res
        fact = factorial(n)
        num_digits = ceil(math.log(fact, 10))
        return first_true(0, num_digits, lambda x: fact != (fact // 10 ** x) * 10 ** x) - 1


sol = Solution()
print(sol.trailingZeroes(100))
print(sol.trailingZeroes(3))
_l, _r = sol.trailingZeroes(3), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.trailingZeroes(5), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.trailingZeroes(0), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.trailingZeroes(1), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.trailingZeroes(4), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.trailingZeroes(10), 2
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.trailingZeroes(25), 6
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.trailingZeroes(50), 12
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.trailingZeroes(100), 24
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.trailingZeroes(125), 31
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.trailingZeroes(1000), 249
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.trailingZeroes(5000), 1249
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.trailingZeroes(10000), 2499
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.trailingZeroes(9999), 2495
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.trailingZeroes(624), 152
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
