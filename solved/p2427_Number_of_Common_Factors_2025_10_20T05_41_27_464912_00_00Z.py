"""
URL: https://leetcode.com/problems/number-of-common-factors/description/?envType=problem-list-v2&envId=vn57k9wr

2427. Number of Common Factors

Given two positive integers a and b, return the number of common factors of a and b.

An integer x is a common factor of a and b if x divides both a and b.


Example 1:

Input: a = 12, b = 6
Output: 4
Explanation: The common factors of 12 and 6 are 1, 2, 3, 6.

Example 2:

Input: a = 25, b = 30
Output: 2
Explanation: The common factors of 25 and 30 are 1, 5.


Constraints:

        1 <= a, b <= 1000
"""

from math import gcd


class Solution:
    def commonFactors(self, a: int, b: int) -> int:
        _gcd = gcd(a, b)
        return len([x for x in range(1, _gcd + 1) if a % x == 0 and b % x == 0])


sol = Solution()
res = sol.commonFactors(a=12, b=6)
assert res == 4

assert sol.commonFactors(a=25, b=30) == 2
