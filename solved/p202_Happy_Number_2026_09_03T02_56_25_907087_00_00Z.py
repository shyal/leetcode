"""
URL: https://leetcode.com/problems/happy-number/description/?envType=problem-list-v2&envId=vn57k9wr

202. Happy Number

Write an algorithm to determine if a number n is happy.

A happy number is a number defined by the following process:

- Starting with any positive integer, replace the number by the sum of the squares of its digits.
- Repeat the process until the number equals 1 (where it will stay), or it loops endlessly in a cycle which does not include 1.
- Those numbers for which this process ends in 1 are happy.

Return true if n is a happy number, and false if not.

Example 1:

Input: n = 19
Output: true
Explanation:
1² + 9² = 82
8² + 2² = 68
6² + 8² = 100
1² + 0² + 0² = 1

Example 2:

Input: n = 2
Output: false

Constraints:

    1 <= n <= 2^31 - 1
"""


class Solution:

    def getDigits(self, num):
        digits = []
        while num:
            digits.append(num % 10)
            num //= 10
        return digits

    def isHappy(self, n: int) -> bool:

        seen = set()

        def helper(x):
            digits = self.getDigits(x)
            n = sum(x**2 for x in digits)
            if n in seen:
                return False
            seen.add(n)
            print(n)
            if n == 1:
                return True
            else:
                return helper(n)

        return helper(n)


sol = Solution()

print(sol.isHappy(19))  # True
print(sol.isHappy(2))  # False

assert sol.isHappy(19) is True
assert sol.isHappy(2) is False

assert sol.isHappy(1) == True
assert sol.isHappy(7) == True
assert sol.isHappy(10) == True
assert sol.isHappy(100) == True
assert sol.isHappy(0) == False
assert sol.isHappy(9999999) == False
assert sol.isHappy(123456789) == False
assert sol.isHappy(4444) == False
assert sol.isHappy(86) == True
assert sol.isHappy(2147483647) == False
assert sol.isHappy(1111111) == True
assert sol.isHappy(3) == False
