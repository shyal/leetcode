"""
URL: https://leetcode.com/problems/move-zeroes/description/?envType=problem-list-v2&envId=vn57k9wr

283. Move Zeroes

Given an integer array nums, move all 0's to the end of it while maintaining
the relative order of the non-zero elements.

Note that you must do this in-place without making a copy of the array.


Example 1:

Input: nums = [0,1,0,3,12]
Output: [1,3,12,0,0]

Example 2:

Input: nums = [0]
Output: [0]


Constraints:

    1 <= nums.length <= 10^4
    -2^31 <= nums[i] <= 2^31 - 1


Follow up: Could you minimize the total number of operations done?
"""


class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        nums.sort(key=lambda x: x == 0)


sol = Solution()

nums = [0, 1, 0, 3, 12]
sol.moveZeroes(nums)
# print(nums)  # [1, 3, 12, 0, 0]

nums = [0, 1, 0, 3, 12]
sol.moveZeroes(nums)
assert nums == [1, 3, 12, 0, 0]

nums = [0]
sol.moveZeroes(nums)
assert nums == [0]

nums = [1]
sol.moveZeroes(nums)
assert nums == [1]

nums = [0, 0, 0]
sol.moveZeroes(nums)
assert nums == [0, 0, 0]

nums = [1, 2, 3]
sol.moveZeroes(nums)
assert nums == [1, 2, 3]

nums = [0, 0, 1]
sol.moveZeroes(nums)
assert nums == [1, 0, 0]

nums = [1, 0]
sol.moveZeroes(nums)
assert nums == [1, 0]

nums = [0, 1]
sol.moveZeroes(nums)
assert nums == [1, 0]

nums = [0, -1, 0, -3]
sol.moveZeroes(nums)
assert nums == [-1, -3, 0, 0]

nums = [1, 0, 1, 0, 1]
sol.moveZeroes(nums)
assert nums == [1, 1, 1, 0, 0]

nums = [4, 2, 4, 0, 0, 3, 0, 5, 1, 0]
sol.moveZeroes(nums)
assert nums == [4, 2, 4, 3, 5, 1, 0, 0, 0, 0]

nums = [-2147483648, 0, 2147483647]
sol.moveZeroes(nums)
assert nums == [-2147483648, 2147483647, 0]

nums = [0, 0, 0, 1]
sol.moveZeroes(nums)
assert nums == [1, 0, 0, 0]

nums = [1, 2, 0, 0]
sol.moveZeroes(nums)
assert nums == [1, 2, 0, 0]

nums = list(range(1, 5001)) + [0] * 5000
expected = list(range(1, 5001)) + [0] * 5000
sol.moveZeroes(nums)
assert nums == expected

nums = [0] * 5000 + list(range(1, 5001))
sol.moveZeroes(nums)
assert nums == list(range(1, 5001)) + [0] * 5000

nums = [0, 1, 0, 3, 12]
alias = nums
sol.moveZeroes(nums)
assert alias is nums
assert alias == [1, 3, 12, 0, 0]

assert sol.moveZeroes([0, 1]) is None