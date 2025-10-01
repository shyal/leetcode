"""
URL: https://leetcode.com/problems/palindrome-number/description/

9. Palindrome Number

Given an integer x, return true if x is a palindrome, and false otherwise.


Example 1:

Input: x = 121
Output: true
Explanation: 121 reads as 121 from left to right and from right to left.

Example 2:

Input: x = -121
Output: false
Explanation: From left to right, it reads -121. From right to left, it becomes 121-. Therefore it is not a palindrome.

Example 3:

Input: x = 10
Output: false
Explanation: Reads 01 from right to left. Therefore it is not a palindrome.


Constraints:

    -231 <= x <= 231 - 1


Follow up: Could you solve it without converting the integer to a string?
"""


class Solution:
    def isPalindrome(self, x: int) -> bool:
        neg = x < 0
        if neg:
            return False

        st = str(x)
        for i in range(len(st) // 2):
            if st[i] != st[len(st) - i - 1]:
                return False
        return True


sol = Solution()

assert sol.isPalindrome(1000021) == False
assert sol.isPalindrome(1000021) == False
assert sol.isPalindrome(-121) == False
assert sol.isPalindrome(121) == True
assert sol.isPalindrome(8228) == True
assert sol.isPalindrome(821128) == True
assert sol.isPalindrome(8215128) == True
assert sol.isPalindrome(82155128) == True
assert sol.isPalindrome(8215995128) == True
assert sol.isPalindrome(10) == False
assert sol.isPalindrome(11) == True
assert sol.isPalindrome(1) == True


