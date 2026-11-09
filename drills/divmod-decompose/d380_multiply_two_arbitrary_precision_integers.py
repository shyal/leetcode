"""
EPI 5.3 Multiply two arbitrary-precision integers

Given two lists of decimal digits num1 and num2 that each represent an
integer, most significant digit first, return the digits of their
product in the same form. A negative integer has its first digit
negative: [-7, 6] is -76.

Example 1:

Input: num1 = [1, 2, 3], num2 = [9, 8, 7]
Output: [1, 2, 1, 4, 0, 1]
Explanation: 123 * 987 = 121401.

Example 2:

Input: num1 = [-1, 2], num2 = [3, 4]
Output: [-4, 0, 8]
Explanation: -12 * 34 = -408.

Example 3:

Input: num1 = [-9, 9], num2 = [0]
Output: [0]
Explanation: The product is 0, and 0 has no sign.

Constraints:

    1 <= len(num1), len(num2) <= 500
    -9 <= num1[0], num2[0] <= 9
    0 <= every other digit <= 9
    No leading zeros, except in [0].

    REQUIRED: O(n * m) time, where n = len(num1) and m = len(num2).
    NO int(), NO str().
"""


class Solution:
    def multiply(self, num1: list[int], num2: list[int]) -> list[int]:
        pass


sol = Solution()

print(sol.multiply([1, 2, 3], [9, 8, 7]))  # [1, 2, 1, 4, 0, 1]

# assert sol.multiply([1, 2, 3], [9, 8, 7]) == [1, 2, 1, 4, 0, 1]
# assert sol.multiply([-1, 2], [3, 4]) == [-4, 0, 8]
# assert sol.multiply([-9, 9], [0]) == [0]
# assert sol.multiply([0], [0]) == [0]
# assert sol.multiply([0], [-5]) == [0]
# assert sol.multiply([1], [1]) == [1]
# assert sol.multiply([-1], [1]) == [-1]
# assert sol.multiply([9], [9]) == [8, 1]
# assert sol.multiply([5], [-2]) == [-1, 0]
# assert sol.multiply([-9, 9], [-9, 9]) == [9, 8, 0, 1]
# assert sol.multiply([2, 5], [4]) == [1, 0, 0]
# assert sol.multiply([1, 0, 0], [1, 0]) == [1, 0, 0, 0]
# assert sol.multiply([1, 9, 3, 7, 0, 7, 7, 2, 1], [-7, 6, 1, 8, 3, 8, 2, 5, 7, 2, 8, 7]) == [-1, 4, 7, 5, 7, 3, 9, 5, 2, 5, 8, 9, 6, 7, 6, 4, 1, 2, 9, 2, 7]
# assert sol.multiply([9] * 500, [9] * 500) == [9] * 499 + [8] + [0] * 499 + [1]
# assert sol.multiply([-9] + [9] * 499, [9] * 500) == [-9] + [9] * 498 + [8] + [0] * 499 + [1]
# assert sol.multiply([1] + [0] * 499, [-1] + [0] * 499) == [-1] + [0] * 998
