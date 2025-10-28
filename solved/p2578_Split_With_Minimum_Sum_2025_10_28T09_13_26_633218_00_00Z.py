"""
URL: https://leetcode.com/problems/split-with-minimum-sum/description/?envType=problem-list-v2&envId=vn57k9wr

2578. Split With Minimum Sum

Given a positive integer num, split it into two non-negative integers num1 and num2 such that:

- The concatenation of num1 and num2 is a permutation of num.
  - In other words, the sum of the number of occurrences of each digit in num1 and num2 is equal to the number of occurrences of that digit in num.
- num1 and num2 can contain leading zeros.

Return the minimum possible sum of num1 and num2.

Notes:
- It is guaranteed that num does not contain any leading zeros.
- The order of occurrence of the digits in num1 and num2 may differ from the order of occurrence of num.

Example 1:

Input: num = 4325
Output: 59
Explanation: We can split 4325 so that num1 is 24 and num2 is 35, giving a sum of 59. We can prove that 59 is indeed the minimal possible sum.

Example 2:

Input: num = 687
Output: 75
Explanation: We can split 687 so that num1 is 68 and num2 is 7, which would give an optimal sum of 75.

Constraints:

    10 <= num <= 10^9
"""


class Solution:
    def getDigits(self, num):
        digits = []
        while num:
            digits.append(num % 10)
            num //= 10
        return digits

    def splitNum(self, num: int) -> int:
        digits = self.getDigits(num)
        digits.sort()
        a, b = 0, 0
        for i, d in enumerate(digits):
            if i % 2 == 0:
                a = a * 10 + d
            else:
                b = b * 10 + d
        return a + b


sol = Solution()

# print(sol.splitNum(4325))  # 59

assert sol.splitNum(4325) == 59
assert sol.splitNum(687) == 75
assert sol.splitNum(10) == 1
assert sol.splitNum(11) == 2
assert sol.splitNum(100) == 1
assert sol.splitNum(101) == 2
assert sol.splitNum(20) == 2
assert sol.splitNum(999) == 108
assert sol.splitNum(1000000000) == 1
assert sol.splitNum(999999999) == 109998
assert sol.splitNum(1234) == 37
assert sol.splitNum(102) == 3
assert sol.splitNum(1001) == 2
assert sol.splitNum(100000000) == 1
