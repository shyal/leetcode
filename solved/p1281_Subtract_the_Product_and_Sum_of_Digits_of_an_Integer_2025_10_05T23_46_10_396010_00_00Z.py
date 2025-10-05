"""
URL: https://leetcode.com/problems/subtract-the-product-and-sum-of-digits-of-an-integer/description/?envType=problem-list-v2&envId=vn57k9wr

1281. Subtract the Product and Sum of Digits of an Integer

Given an integer number n, return the difference between the product of its digits and the sum of its digits.

Example 1:

Input: n = 234
Output: 15
Explanation: Product of digits = 2 * 3 * 4 = 24
Sum of digits = 2 + 3 + 4 = 9
Result = 24 - 9 = 15

Example 2:

Input: n = 4421
Output: 21
Explanation: Product of digits = 4 * 4 * 2 * 1 = 32
Sum of digits = 4 + 4 + 2 + 1 = 11
Result = 32 - 11 = 21

Constraints:

    1 <= n <= 10^5
"""


class Solution:
    def subtractProductAndSum(self, n: int) -> int:

        def get_digits(n):
            digits = []
            while n:
                digits.append(n % 10)
                n //= 10
            return digits

        digits = get_digits(n)

        return prod(digits) - sum(digits)


sol = Solution()

assert sol.subtractProductAndSum(234) == 15
assert sol.subtractProductAndSum(4421) == 21
assert sol.subtractProductAndSum(1) == 0
assert sol.subtractProductAndSum(10) == -1
assert sol.subtractProductAndSum(11) == -1
assert sol.subtractProductAndSum(99999) == 59004
assert sol.subtractProductAndSum(100000) == -1
assert sol.subtractProductAndSum(12345) == 105
assert sol.subtractProductAndSum(20) == -2
assert sol.subtractProductAndSum(5) == 0
assert sol.subtractProductAndSum(100) == -1
