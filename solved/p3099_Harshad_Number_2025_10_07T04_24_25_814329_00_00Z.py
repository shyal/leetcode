"""
URL: https://leetcode.com/problems/harshad-number/description/

3099. Harshad Number

An integer divisible by the sum of its digits is called a Harshad number. You are given an integer x. Return the sum of the digits of x if x is a Harshad number, otherwise, return -1.

Example 1:

Input: x = 18
Output: 9
Explanation: The sum of digits of 18 is 9. 18 is divisible by 9. So return 9.

Example 2:

Input: x = 23
Output: -1
Explanation: The sum of digits of 23 is 5. 23 is not divisible by 5. So return -1.

Constraints:

    1 <= x <= 100
"""


class Solution:
    def sumOfTheDigitsOfHarshadNumber(self, x: int) -> int:
        harshad = lambda x: sum(int(y) for y in str(x))
        is_harshad = lambda x, h: x % h == 0
        h = harshad(x)
        return h if is_harshad(x, h) else -1


sol = Solution()

# print(sol.harshadNumber(18))  # 9

assert sol.harshadNumber(18) == 9
assert sol.harshadNumber(23) == -1
assert sol.harshadNumber(1) == 1
assert sol.harshadNumber(9) == 9
assert sol.harshadNumber(10) == 1
assert sol.harshadNumber(11) == -1
assert sol.harshadNumber(20) == 2
assert sol.harshadNumber(22) == -1
assert sol.harshadNumber(81) == 9
assert sol.harshadNumber(99) == -1
assert sol.harshadNumber(100) == 1
