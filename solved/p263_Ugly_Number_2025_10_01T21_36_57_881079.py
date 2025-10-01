"""
URL: https://leetcode.com/problems/ugly-number/description/?envType=problem-list-v2&envId=vn57k9wr

263. Ugly Number

An ugly number is a positive integer which does not have a prime factor other than 2, 3, and 5.

Given an integer n, return true if n is an ugly number.

Example 1:

Input: n = 6
Output: true
Explanation: 6 = 2 x 3

Example 2:

Input: n = 1
Output: true
Explanation: 1 has no prime factors.

Example 3:

Input: n = 14
Output: false
Explanation: 14 is not ugly since it includes the prime factor 7.

Constraints:

    -2^31 <= n <= 2^31 - 1
"""


class Solution:
    def isUgly(self, n: int) -> bool:
        if n == 0:
            return False
        if n == 1:
            return True
        v = n
        while v != 1:
            for d in [2, 3, 5]:
                if v % d == 0:
                    v = v // d
                    break
            else:
                return False
        return True


sol = Solution()
assert sol.isUgly(0) == False
assert sol.isUgly(6) == True
assert sol.isUgly(1) == True
assert sol.isUgly(14) == False
assert sol.isUgly(6) == True
assert sol.isUgly(1) == True
assert sol.isUgly(14) == False
assert sol.isUgly(2) == True
assert sol.isUgly(3) == True
assert sol.isUgly(4) == True
assert sol.isUgly(5) == True
assert sol.isUgly(7) == False
assert sol.isUgly(8) == True
assert sol.isUgly(9) == True
assert sol.isUgly(10) == True
assert sol.isUgly(11) == False
assert sol.isUgly(12) == True
assert sol.isUgly(15) == True
assert sol.isUgly(16) == True
assert sol.isUgly(21) == False
assert sol.isUgly(25) == True
assert sol.isUgly(27) == True
assert sol.isUgly(30) == True
assert sol.isUgly(2147483647) == False
