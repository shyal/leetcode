"""
URL: https://leetcode.com/problems/n-th-tribonacci-number/description/?envType=problem-list-v2&envId=vn57k9wr

1137. N-th Tribonacci Number

The Tribonacci sequence T_n is defined as follows:

T_0 = 0, T_1 = 1, T_2 = 1, and T_{n+3} = T_n + T_{n+1} + T_{n+2} for n >= 0.

Given n, return the value of T_n.

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


class Solution:
    def tribonacci(self, n: int) -> int:
        # T0 = 0, T1 = 1, T2 = 1, and Tn+3 = Tn + Tn+1 + Tn+2 for n >= 0.

        @cache
        def tri(n):
            if n <= 1:
                return n
            elif n == 2:
                return 1
            return tri(n - 3) + tri(n - 2) + tri(n - 1)

        return tri(n)


sol = Solution()

print(sol.tribonacci(4))  # 4

assert sol.tribonacci(4) == 4
assert sol.tribonacci(25) == 1389537

assert sol.tribonacci(0) == 0
assert sol.tribonacci(1) == 1
assert sol.tribonacci(2) == 1
assert sol.tribonacci(3) == 2
assert sol.tribonacci(10) == 149
assert sol.tribonacci(20) == 66012
assert sol.tribonacci(37) == 2082876103
assert sol.tribonacci(5) == 7
assert sol.tribonacci(6) == 13
assert sol.tribonacci(7) == 24
assert sol.tribonacci(8) == 44
assert sol.tribonacci(9) == 81
