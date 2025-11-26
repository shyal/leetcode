"""
URL: https://leetcode.com/problems/binary-prefix-divisible-by-5/description/?envType=problem-list-v2&envId=vn57k9wr

1018. Binary Prefix Divisible By 5

You are given a binary array nums (0-indexed).

We define x_i as the number whose binary representation is the subarray nums[0..i] (from most-significant-bit to least-significant-bit).

For example, if nums = [1,0,1], then x_0 = 1, x_1 = 2, and x_2 = 5.

Return an array of booleans answer where answer[i] is true if x_i is divisible by 5.


Example 1:

Input: nums = [0,1,1]
Output: [true,false,false]
Explanation: The input numbers in binary are 0, 01, 011; which are 0, 1, and 3 in base-10.
Only the first number is divisible by 5, so answer[0] is true.

Example 2:

Input: nums = [1,1,1]
Output: [false,false,false]


Constraints:

    1 <= nums.length <= 10^5
    nums[i] is either 0 or 1.
"""

class Solution:
    def prefixesDivBy5(self, nums: List[int]) -> List[bool]:
        prefix = 0
        for i, n in enumerate(nums):
            prefix = prefix * 2 + n
            nums[i] = bool(prefix % 5 == 0)
        return nums

sol = Solution()

# print(sol.prefixesDivBy5([0,1,1]))  # [True, False, False]

assert sol.prefixesDivBy5([0,1,1]) == [True, False, False]
assert sol.prefixesDivBy5([1,1,1]) == [False, False, False]
assert sol.prefixesDivBy5([0]) == [True]
assert sol.prefixesDivBy5([1]) == [False]
assert sol.prefixesDivBy5([1,0,1]) == [False, False, True]
assert sol.prefixesDivBy5([0,0,0]) == [True, True, True]
assert sol.prefixesDivBy5([1,1,1,1]) == [False, False, False, True]
assert sol.prefixesDivBy5([1,0,1,0]) == [False, False, True, True]
assert sol.prefixesDivBy5([1,0,1,1]) == [False, False, True, False]