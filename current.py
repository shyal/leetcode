"""
URL: https://leetcode.com/problems/happy-number/description/

202. Happy Number

Write an algorithm to determine if a number n is happy.

A happy number is a number defined by the following process:

        Starting with any positive integer, replace the number by the sum of the squares of its digits.
        Repeat the process until the number equals 1 (where it will stay), or it loops endlessly in a cycle which does not include 1.
        Those numbers for which this process ends in 1 are happy.

Return true if n is a happy number, and false if not.


Example 1:

Input: n = 19
Output: true
Explanation:
1^2 + 9^2 = 82
8^2 + 2^2 = 68
6^2 + 8^2 = 100
1^2 + 0^2 + 02 = 1

Example 2:

Input: n = 2
Output: false


Constraints:

        1 <= n <= 231 - 1
"""

from functools import reduce


class Solution:
    def isHappy(self, n: int) -> bool:
        nums = set([])
        while n != 1:
            digits = [int(x) for x in str(n)]
            n = reduce(lambda acc, v: acc + v * v, digits, 0)
            nums_size = len(nums)
            nums.add(n)
            if nums_size == len(nums):
                break
        return n == 1


sol = Solution()

assert sol.isHappy(19) == True
assert sol.isHappy(2) == False
assert sol.isHappy(19) == True
assert sol.isHappy(2) == False
assert sol.isHappy(1) == True
assert sol.isHappy(7) == True
assert sol.isHappy(4) == False
assert sol.isHappy(10) == True
assert sol.isHappy(1111111) == True
assert sol.isHappy(9999999) == False
assert sol.isHappy(2147483647) == False
assert sol.isHappy(1000000000) == True
assert sol.isHappy(13) == True
assert sol.isHappy(11) == False
assert sol.isHappy(44) == True
