"""
URL: https://leetcode.com/problems/maximum-difference-by-remapping-a-digit/description/?envType=problem-list-v2&envId=vn57k9wr

2566. Maximum Difference by Remapping a Digit

You are given an integer num. You know that Bob will sneakily remap one of the 10 possible digits (0 to 9) to another digit.

Return the difference between the maximum and minimum values Bob can make by remapping exactly one digit in num.

Notes:

- When Bob remaps a digit d1 to another digit d2, Bob replaces all occurrences of d1 in num with d2.
- Bob can remap a digit to itself, in which case num does not change.
- Bob can remap different digits for obtaining minimum and maximum values respectively.
- The resulting number after remapping can contain leading zeroes.

Example 1:

Input: num = 11891
Output: 99009
Explanation:
To achieve the maximum value, Bob can remap the digit 1 to the digit 9 to yield 99899.
To achieve the minimum value, Bob can remap the digit 1 to the digit 0, yielding 890.
The difference between these two numbers is 99009.

Example 2:

Input: num = 90
Output: 99
Explanation:
The maximum value that can be returned by the function is 99 (if 0 is replaced by 9) and the minimum value that can be returned by the function is 0 (if 9 is replaced by 0).
Thus, we return 99.

Constraints:

- 1 <= num <= 10^8
---
For the maximum digit, get the right most digit that is not a 9.

"""


class Solution:
    def getDigits(self, num):
        digits = []
        while num:
            digits.append(num % 10)
            num //= 10
        return digits[::-1]

    def digitsToNum(self, digits):
        res = 0
        for d in digits:
            res = res * 10 + d
        return res

    def findFirstNonZero(self, digits):
        for i, d in enumerate(digits):
            if d != 0:
                return d

    def findFirstNonNine(self, digits):
        for i, d in enumerate(digits):
            if d != 9:
                return d

    def minMaxDifference(self, num: int) -> int:
        digits = self.getDigits(num)
        max_digit = digits[:]
        min_digit = digits[:]
        _min = self.findFirstNonNine(digits)
        _max = self.findFirstNonZero(digits)
        for i, d in enumerate(digits):
            if d == _min:
                max_digit[i] = 9
        for i, d in enumerate(digits):
            if d == _max:
                min_digit[i] = 0
        return self.digitsToNum(max_digit) - self.digitsToNum(min_digit)


sol = Solution()

assert sol.minMaxDifference(11891) == 99009
assert sol.minMaxDifference(90) == 99
assert sol.minMaxDifference(1) == 9
assert sol.minMaxDifference(9) == 9
assert sol.minMaxDifference(10) == 90
assert sol.minMaxDifference(100) == 900
assert sol.minMaxDifference(999) == 999
assert sol.minMaxDifference(100000000) == 900000000
assert sol.minMaxDifference(123) == 900
assert sol.minMaxDifference(21) == 90
assert sol.minMaxDifference(9991) == 9998
assert sol.minMaxDifference(11111111) == 99999999
