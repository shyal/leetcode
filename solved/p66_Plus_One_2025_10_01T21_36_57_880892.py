"""
URL: https://leetcode.com/problems/plus-one/description/

66. Plus One

You are given a large integer represented as an integer array digits, where each digits[i] is the ith digit of the integer. The digits are ordered from most significant to least significant in left-to-right order. The large integer does not contain any leading 0's.

Increment the large integer by one and return the resulting array of digits.


Example 1:

Input: digits = [1,2,3]
Output: [1,2,4]
Explanation: The array represents the integer 123.
Incrementing by one gives 123 + 1 = 124.
Thus, the result should be [1,2,4].

Example 2:

Input: digits = [4,3,2,1]
Output: [4,3,2,2]
Explanation: The array represents the integer 4321.
Incrementing by one gives 4321 + 1 = 4322.
Thus, the result should be [4,3,2,2].

Example 3:

Input: digits = [9]
Output: [1,0]
Explanation: The array represents the integer 9.
Incrementing by one gives 9 + 1 = 10.
Thus, the result should be [1,0].


Constraints:

    1 <= digits.length <= 100
    0 <= digits[i] <= 9
    digits does not contain any leading 0's.

--------

1 2 3

This case is easy, we just add to the digits[-1] the problem arises if it's 9

1 2 9

In this case, we need to set digits[-1] to 0

1 2 0

then focus on the second to last element, and increment it

1 3 0

so the real edgecase is when it's all 9s

9 9 9

- carry = False
- iterate from right to left
    - if it's the last index:
        - if d < 9
            - add 1
        - else
            - carry = True
            - d = 0
    - elif carry:
        - if d == 9
            - d = 0
    - elif not carry:
        break

- if nums[0] == 0
    - insert 0 at front of digits

"""


class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        carry = False
        for i in range(len(digits) - 1, -1, -1):
            d = digits[i]
            is_end = i == len(digits) - 1
            if is_end:
                if d < 9:
                    digits[i] += 1
                else:
                    carry = True
                    digits[i] = 0
            elif carry:
                if d == 9:
                    digits[i] = 0
                    carry = True
                else:
                    digits[i] += 1
                    carry = False
            elif not carry:
                break

        if digits[0] == 0:
            digits.insert(0, 1)

        return digits


sol = Solution()
assert sol.plusOne([1, 2, 3]) == [1, 2, 4]
assert sol.plusOne([4, 3, 2, 1]) == [4, 3, 2, 2]
assert sol.plusOne([0]) == [1]
assert sol.plusOne([1]) == [2]
assert sol.plusOne([9]) == [1, 0]
assert sol.plusOne([9, 9]) == [1, 0, 0]
assert sol.plusOne([1, 9, 9]) == [2, 0, 0]
assert sol.plusOne([1, 1, 9, 9]) == [1, 2, 0, 0]
assert sol.plusOne([9, 9, 9, 9]) == [1, 0, 0, 0, 0]


