"""
URL: https://leetcode.com/problems/bitwise-or-of-even-numbers-in-an-array/description/?envType=problem-list-v2&envId=v0n2n1sc

3688. Bitwise OR of Even Numbers in an Array

You are given an integer array nums.

Return the bitwise OR of all even numbers in the array.

If there are no even numbers in nums, return 0.


Example 1:

Input: nums = [1,2,3,4,5,6]

Output: 6

Explanation:

The even numbers are 2, 4, and 6. Their bitwise OR equals 6.

Example 2:

Input: nums = [7,9,11]

Output: 0

Explanation:

There are no even numbers, so the result is 0.

Example 3:

Input: nums = [1,8,16]

Output: 24

Explanation:

The even numbers are 8 and 16. Their bitwise OR equals 24.


Constraints:

        1 <= nums.length <= 100
        1 <= nums[i] <= 100

"""


class Solution:
    def evenNumberBitwiseORs(self, nums: List[int]) -> int:
        return reduce(or_, filter(lambda x: x % 2 == 0, nums), 0)


sol = Solution()
assert sol.evenNumberBitwiseORs(nums=[1, 2, 3, 4, 5, 6]) == 6
assert sol.evenNumberBitwiseORs(nums=[7, 9, 11]) == 0
assert sol.evenNumberBitwiseORs(nums=[1, 8, 16]) == 24
