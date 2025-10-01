"""
283. Move Zeroes
Easy
Given an integer array nums, move all 0's to the end of it while maintaining the relative order of the non-zero elements.

Note that you must do this in-place without making a copy of the array.

Example 1:

Input: nums = [0,1,0,3,12]
Output: [1,3,12,0,0]
Example 2:

Input: nums = [0]
Output: [0]
 

Constraints:

1 <= nums.length <= 104
-231 <= nums[i] <= 231 - 1
 

Follow up: Could you minimize the total number of operations done?
"""


class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        write = 0
        for read in range(len(nums)):
            if nums[read] != 0:
                nums[write], nums[read] = nums[read], nums[write]
                write += 1


sol = Solution()
nums = [0, 1, 0, 3, 12]
sol.moveZeroes(nums=nums)

nums = [0, 1, 0, 3, 12]
sol.moveZeroes(nums)
assert nums == [1, 3, 12, 0, 0]

nums = [0]
sol.moveZeroes(nums)
assert nums == [0]

nums = [1, 2, 3, 4, 5]
sol.moveZeroes(nums)
assert nums == [1, 2, 3, 4, 5]

nums = [0, 0, 0, 0]
sol.moveZeroes(nums)
assert nums == [0, 0, 0, 0]

nums = [1, 2, 3, 0, 0]
sol.moveZeroes(nums)
assert nums == [1, 2, 3, 0, 0]

nums = [0, 0, 1, 2, 3]
sol.moveZeroes(nums)
assert nums == [1, 2, 3, 0, 0]

nums = [0, 1, 0, 2, 0, 3, 0, 4]
sol.moveZeroes(nums)
assert nums == [1, 2, 3, 4, 0, 0, 0, 0]

nums = [0, -1, 0, -2, -3, 0]
sol.moveZeroes(nums)
assert nums == [-1, -2, -3, 0, 0, 0]

nums = [7]
sol.moveZeroes(nums)
assert nums == [7]

nums = [0, 5, 0, 0, 9, 8, 0, 7, 0, 6, 0, 0, 10]
sol.moveZeroes(nums)
assert nums == [5, 9, 8, 7, 6, 10, 0, 0, 0, 0, 0, 0, 0]


