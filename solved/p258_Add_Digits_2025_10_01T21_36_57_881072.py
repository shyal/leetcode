"""
URL: https://leetcode.com/problems/add-digits/description/?envType=problem-list-v2&envId=vn57k9wr

258. Add Digits

Given an integer num, repeatedly add all its digits until the result has only one digit, and return it.


Example 1:

Input: num = 38
Output: 2
Explanation: The process is
38 --> 3 + 8 --> 11
11 --> 1 + 1 --> 2
Since 2 has only one digit, return it.

Example 2:

Input: num = 0
Output: 0


Constraints:

        0 <= num <= 231 - 1


Follow up: Could you do it without any loop/recursion in O(1) runtime?
"""


class Solution:
    def addDigits(self, num: int) -> int:
        while num >= 10:
            num = sum(int(x) for x in str(num))
        return num


sol = Solution()
assert sol.addDigits(38) == 2

sol = Solution()
assert sol.addDigits(0) == 0

sol = Solution()
assert sol.addDigits(3887612) == 8

sol = Solution()
assert sol.addDigits(10) == 1
