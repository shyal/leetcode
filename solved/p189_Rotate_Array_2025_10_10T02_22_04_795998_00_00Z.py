"""
URL: https://leetcode.com/problems/rotate-array/description/

189. Rotate Array

Given an integer array nums, rotate the array to the right by k steps, where k is non-negative.


Example 1:

Input: nums = [1,2,3,4,5,6,7], k = 3
Output: [5,6,7,1,2,3,4]
Explanation:
rotate 1 steps to the right: [7,1,2,3,4,5,6]
rotate 2 steps to the right: [6,7,1,2,3,4,5]
rotate 3 steps to the right: [5,6,7,1,2,3,4]

Example 2:

Input: nums = [-1,-100,3,99], k = 2
Output: [3,99,-1,-100]
Explanation:
rotate 1 steps to the right: [99,-1,-100,3]
rotate 2 steps to the right: [3,99,-1,-100]


Constraints:

    1 <= nums.length <= 105
    -231 <= nums[i] <= 231 - 1
    0 <= k <= 105


Follow up:

    Try to come up with as many solutions as you can. There are at least three different ways to solve this problem.
    Could you do it in-place with O(1) extra space?

"""


class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        n = len(nums)
        k = k % n
        if 0 < k < n:
            nums[:] = nums[n - k :] + nums[: n - k]


sol = Solution()

nums = [1, 2, 3, 4, 5, 6, 7]
sol.rotate(nums, 3)
# print(nums)
assert nums == [5, 6, 7, 1, 2, 3, 4]
nums = [-1, -100, 3, 99]
sol.rotate(nums, 2)
assert nums == [3, 99, -1, -100]
nums = [1]
sol.rotate(nums, 0)
assert nums == [1]
nums = [1]
sol.rotate(nums, 1)
assert nums == [1]
nums = [1]
sol.rotate(nums, 105)
assert nums == [1]
nums = [1, 2]
sol.rotate(nums, 1)
assert nums == [2, 1]
nums = [1, 2]
sol.rotate(nums, 2)
assert nums == [1, 2]
nums = [1, 2]
sol.rotate(nums, 3)
assert nums == [2, 1]
nums = [1, 2, 3, 4]
sol.rotate(nums, 0)
assert nums == [1, 2, 3, 4]
nums = [-1]
sol.rotate(nums, 5)
assert nums == [-1]
nums = [0, 0, 0]
sol.rotate(nums, 2)
assert nums == [0, 0, 0]
nums = [1, 2, 3, 4, 5]
sol.rotate(nums, 2)
assert nums == [4, 5, 1, 2, 3]
nums = [1, 2, 3, 4, 5]
sol.rotate(nums, 4)
assert nums == [2, 3, 4, 5, 1]
nums = [-2147483648, 2147483647]
sol.rotate(nums, 1)
assert nums == [2147483647, -2147483648]
nums = [1, 2, 3, 4, 5, 6]
sol.rotate(nums, 3)
assert nums == [4, 5, 6, 1, 2, 3]
nums = [1, 2, 3, 4, 5, 6]
sol.rotate(nums, 6)
assert nums == [1, 2, 3, 4, 5, 6]
nums = [1, 2, 3, 4, 5, 6]
sol.rotate(nums, 7)
assert nums == [6, 1, 2, 3, 4, 5]
