"""
URL: https://leetcode.com/problems/count-integers-with-even-digit-sum/description/?envType=problem-list-v2&envId=vn57k9wr

2180. Count Integers With Even Digit Sum

Given a positive integer num, return the number of positive integers less than or equal to num whose digit sums are even.

The digit sum of a positive integer is the sum of all its digits.

Example 1:

Input: num = 4
Output: 2
Explanation:
The only integers less than or equal to 4 whose digit sums are even are 2 and 4.

Example 2:

Input: num = 30
Output: 14
Explanation:
The 14 integers less than or equal to 30 whose digit sums are even are
2, 4, 6, 8, 11, 13, 15, 17, 19, 20, 22, 24, 26, and 28.

Constraints:

    1 <= num <= 1000
"""


class Solution:

    def getDigits(self, num):
        digits = []
        while num:
            digits.append(num % 10)
            num //= 10
        return digits

    def digitSum(self, x):
        return sum(self.getDigits(x))

    def countEven(self, num: int) -> int:
        return sum(self.digitSum(x) % 2 == 0 for x in range(1, num + 1))


sol = Solution()

# print(sol.countEven(4))  # 2

assert sol.countEven(4) == 2
assert sol.countEven(30) == 14
assert sol.countEven(1) == 0
assert sol.countEven(2) == 1
assert sol.countEven(10) == 4
assert sol.countEven(11) == 5
assert sol.countEven(100) == 49
assert sol.countEven(999) == 499
assert sol.countEven(1000) == 499
