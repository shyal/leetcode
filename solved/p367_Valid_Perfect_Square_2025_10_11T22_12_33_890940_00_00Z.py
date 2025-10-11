"""
URL: https://leetcode.com/problems/valid-perfect-square/description/

367. Valid Perfect Square

Given a positive integer num, return true if num is a perfect square or false otherwise.

A perfect square is an integer that is the square of an integer. For example, 1, 4, 9, and 16 are perfect squares while 3 and 11 are not.


Example 1:

Input: num = 16
Output: true

Example 2:

Input: num = 14
Output: false


Constraints:

    1 <= num <= 2^31 - 1

"""


class Solution:
    def isPerfectSquare(self, num: int) -> bool:
        low = 1
        high = num

        while low <= high:
            mid = low + (high - low) // 2
            guess = mid * mid
            if guess == num:
                return True
            elif guess < num:
                low = mid + 1
            else:
                high = mid - 1

        return False


sol = Solution()

# print(sol.isPerfectSquare(16))  # True

assert sol.isPerfectSquare(16) == True
assert sol.isPerfectSquare(14) == False
assert sol.isPerfectSquare(1) == True
assert sol.isPerfectSquare(0) == False
assert sol.isPerfectSquare(4) == True
assert sol.isPerfectSquare(2) == False
assert sol.isPerfectSquare(9) == True
assert sol.isPerfectSquare(3) == False
assert sol.isPerfectSquare(25) == True
assert sol.isPerfectSquare(26) == False
assert sol.isPerfectSquare(2147395600) == True
assert sol.isPerfectSquare(2147483647) == False
