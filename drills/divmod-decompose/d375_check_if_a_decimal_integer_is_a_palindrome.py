"""
EPI 4.9 Check if a decimal integer is a palindrome

Given an integer x, return True when its decimal representation reads
the same from left to right and from right to left, and False otherwise.
The minus sign is part of the representation, so a negative number is
not a palindrome.

Example 1:

Input: x = 12321
Output: True

Example 2:

Input: x = -121
Output: False
Explanation: from right to left it reads 121-.

Example 3:

Input: x = 10
Output: False

Constraints:

    -2^63 <= x < 2^63

    REQUIRED: O(n) time and O(1) extra space, where n is the number of
    digits of x. NO str(), NO repr(), NO f-string, NO list of digits.
"""


class Solution:
    def is_palindrome_number(self, x: int) -> bool:
        pass


sol = Solution()

print(sol.is_palindrome_number(12321))  # True

# assert sol.is_palindrome_number(12321) is True
# assert sol.is_palindrome_number(-121) is False
# assert sol.is_palindrome_number(10) is False
# assert sol.is_palindrome_number(0) is True
# assert sol.is_palindrome_number(7) is True
# assert sol.is_palindrome_number(-1) is False
# assert sol.is_palindrome_number(11) is True
# assert sol.is_palindrome_number(100) is False
# assert sol.is_palindrome_number(1001) is True
# assert sol.is_palindrome_number(10101) is True
# assert sol.is_palindrome_number(1021) is False
# assert sol.is_palindrome_number(1000021) is False
# assert sol.is_palindrome_number(123454321) is True
# assert sol.is_palindrome_number(9223372036854775807) is False
# assert sol.is_palindrome_number(1234567890987654321) is True
# assert sol.is_palindrome_number(1234567899887654321) is False
