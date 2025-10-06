"""
URL: https://leetcode.com/problems/count-the-digits-that-divide-a-number/description/?envType=problem-list-v2&envId=vn57k9wr

2520. Count the Digits That Divide a Number

Given an integer num, return the number of digits in num that divide num.

An integer val divides num if num % val == 0.


Example 1:

Input: num = 7
Output: 1
Explanation: 7 divides itself, so the answer is 1.

Example 2:

Input: num = 121
Output: 2
Explanation: 121 is divisible by 1, but not 2. Since 1 appears twice as a digit, return 2.

Example 3:

Input: num = 1248
Output: 4
Explanation: 1248 is divisible by 1, 2, 4, 8.


Constraints:

    1 <= num <= 10^9
    num does not contain 0 as one of its digits.
"""


class Solution:

    def getDigits(self, num):
        digits = []
        while num:
            digits.append(num % 10)
            num //= 10
        return digits

    def countDigits(self, num: int) -> int:
        res = 0
        counts = dict(Counter(self.getDigits(num))).items()
        for k, v in counts:
            if num % k == 0:
                res += v
        return res


sol = Solution()

# print(sol.countDigits(7))  # 1

assert sol.countDigits(7) == 1
assert sol.countDigits(121) == 2
assert sol.countDigits(1248) == 4
assert sol.countDigits(1) == 1
assert sol.countDigits(9) == 1
assert sol.countDigits(23) == 0
assert sol.countDigits(27) == 0
assert sol.countDigits(111) == 3
assert sol.countDigits(1111111) == 7
assert sol.countDigits(999999999) == 9
assert sol.countDigits(222222222) == 9
assert sol.countDigits(123456789) == 3
assert sol.countDigits(13579) == 1
assert sol.countDigits(13) == 1
assert sol.countDigits(22) == 2
assert sol.countDigits(25) == 1
assert sol.countDigits(12) == 2
assert sol.countDigits(24) == 2
