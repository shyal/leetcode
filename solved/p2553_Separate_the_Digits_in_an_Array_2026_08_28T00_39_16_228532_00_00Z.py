"""
URL: https://leetcode.com/problems/separate-the-digits-in-an-array/description/?envType=problem-list-v2&envId=vn57k9wr

2553. Separate the Digits in an Array

Given an array of positive integers nums, return an array answer that consists of the digits of each integer in nums after separating them in the same order they appear in nums.

To separate the digits of an integer is to get all the digits it has in the same order.

For example, for the integer 10921, the separation of its digits is [1,0,9,2,1].

Example 1:

Input: nums = [13,25,83,77]
Output: [1,3,2,5,8,3,7,7]
Explanation:
- The separation of 13 is [1,3].
- The separation of 25 is [2,5].
- The separation of 83 is [8,3].
- The separation of 77 is [7,7].
answer = [1,3,2,5,8,3,7,7]. Note that answer contains the separations in the same order.

Example 2:

Input: nums = [7,1,3,9]
Output: [7,1,3,9]
Explanation: The separation of each integer in nums is itself.
answer = [7,1,3,9].

Constraints:

    1 <= nums.length <= 1000
    1 <= nums[i] <= 10^5
"""


class Solution:

    def getDigits(self, num):
        digits = []
        while num:
            digits.append(num % 10)
            num //= 10
        return digits[::-1]

    def separateDigits(self, nums: List[int]) -> List[int]:
        res = [
            *chain.from_iterable(
                chain.from_iterable(zip_longest(self.getDigits(x) for x in nums))
            )
        ]
        return res


sol = Solution()

print(sol.separateDigits([13, 25, 83, 77]))  # [1,3,2,5,8,3,7,7]

assert sol.separateDigits([13, 25, 83, 77]) == [1, 3, 2, 5, 8, 3, 7, 7]
assert sol.separateDigits([7, 1, 3, 9]) == [7, 1, 3, 9]

assert sol.separateDigits([1]) == [1]
assert sol.separateDigits([10]) == [1, 0]
assert sol.separateDigits([100000]) == [1, 0, 0, 0, 0, 0]
assert sol.separateDigits([99999]) == [9, 9, 9, 9, 9]
assert sol.separateDigits([12345, 67890]) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
assert sol.separateDigits([11111, 22222, 33333]) == [
    1,
    1,
    1,
    1,
    1,
    2,
    2,
    2,
    2,
    2,
    3,
    3,
    3,
    3,
    3,
]
assert sol.separateDigits([98765, 43210, 12345]) == [
    9,
    8,
    7,
    6,
    5,
    4,
    3,
    2,
    1,
    0,
    1,
    2,
    3,
    4,
    5,
]
assert sol.separateDigits([1, 22, 333, 4444, 55555]) == [
    1,
    2,
    2,
    3,
    3,
    3,
    4,
    4,
    4,
    4,
    5,
    5,
    5,
    5,
    5,
]
assert sol.separateDigits([100, 200, 300, 400, 500]) == [
    1,
    0,
    0,
    2,
    0,
    0,
    3,
    0,
    0,
    4,
    0,
    0,
    5,
    0,
    0,
]
assert sol.separateDigits([10101, 20202, 30303]) == [
    1,
    0,
    1,
    0,
    1,
    2,
    0,
    2,
    0,
    2,
    3,
    0,
    3,
    0,
    3,
]
