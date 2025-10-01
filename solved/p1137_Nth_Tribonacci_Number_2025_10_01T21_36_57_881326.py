"""
URL: https://leetcode.com/problems/n-th-tribonacci-number/description/?envType=study-plan-v2&envId=leetcode-75

1137. N-th Tribonacci Number

The Tribonacci sequence Tn is defined as follows:

T0 = 0, T1 = 1, T2 = 1, and Tn+3 = Tn + Tn+1 + Tn+2 for n >= 0.

Given n, return the value of Tn.


Example 1:

Input: n = 4
Output: 4
Explanation:
T_3 = 0 + 1 + 1 = 2
T_4 = 1 + 1 + 2 = 4

Example 2:

Input: n = 25
Output: 1389537


Constraints:

        0 <= n <= 37
        The answer is guaranteed to fit within a 32-bit integer, ie. answer <= 2^31 - 1.
"""

from functools import cache


class Solution:
    @cache
    def tribonacci(self, n: int) -> int:
        if n <= 1:
            return n
        elif n == 2:
            return 1
        return self.tribonacci(n - 3) + self.tribonacci(n - 2) + self.tribonacci(n - 1)


sol = Solution()

result = sol.tribonacci(0)
assert result == 0

result = sol.tribonacci(1)
assert result == 1

result = sol.tribonacci(2)
assert result == 1

result = sol.tribonacci(3)
assert result == 2

result = sol.tribonacci(4)
assert result == 4

result = sol.tribonacci(5)
assert result == 7

result = sol.tribonacci(6)
assert result == 13

result = sol.tribonacci(7)
assert result == 24

result = sol.tribonacci(8)
assert result == 44

result = sol.tribonacci(9)
assert result == 81

result = sol.tribonacci(10)
assert result == 149

result = sol.tribonacci(11)
assert result == 274

result = sol.tribonacci(12)
assert result == 504

result = sol.tribonacci(13)
assert result == 927

result = sol.tribonacci(14)
assert result == 1705

result = sol.tribonacci(15)
assert result == 3136

result = sol.tribonacci(16)
assert result == 5768

result = sol.tribonacci(17)
assert result == 10609

result = sol.tribonacci(18)
assert result == 19513

result = sol.tribonacci(19)
assert result == 35890

result = sol.tribonacci(20)
assert result == 66012

result = sol.tribonacci(21)
assert result == 121415

result = sol.tribonacci(22)
assert result == 223317

result = sol.tribonacci(23)
assert result == 410744

result = sol.tribonacci(24)
assert result == 755476

result = sol.tribonacci(25)
assert result == 1389537

result = sol.tribonacci(26)
assert result == 2555757

result = sol.tribonacci(27)
assert result == 4700770

result = sol.tribonacci(28)
assert result == 8646064

result = sol.tribonacci(29)
assert result == 15902591

result = sol.tribonacci(30)
assert result == 29249425

result = sol.tribonacci(31)
assert result == 53798080

result = sol.tribonacci(32)
assert result == 98950096

result = sol.tribonacci(33)
assert result == 181997601

result = sol.tribonacci(34)
assert result == 334745777

result = sol.tribonacci(35)
assert result == 615693474

result = sol.tribonacci(36)
assert result == 1132436852

result = sol.tribonacci(37)
assert result == 2082876103
