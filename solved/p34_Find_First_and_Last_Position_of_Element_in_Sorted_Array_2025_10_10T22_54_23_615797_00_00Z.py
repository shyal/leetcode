"""
URL: https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/description/

34. Find First and Last Position of Element in Sorted Array

Given an array of integers nums sorted in non-decreasing order, find the starting and ending position of a given target value.

If target is not found in the array, return [-1, -1].

You must write an algorithm with O(log n) runtime complexity.

Example 1:

Input: nums = [5,7,7,8,8,10], target = 8
Output: [3,4]

Example 2:

Input: nums = [5,7,7,8,8,10], target = 6
Output: [-1,-1]

Example 3:

Input: nums = [], target = 0
Output: [-1,-1]

Constraints:

    0 <= nums.length <= 10^5
    -10^9 <= nums[i] <= 10^9
    nums is a non-decreasing array.
    -10^9 <= target <= 10^9

"""


class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        def start():
            left = bisect_left(nums, target)
            if 0 <= left < len(nums):
                if nums[left] == target:
                    return left
            return -1

        def end():
            right = bisect_right(nums, target) - 1
            if 0 <= right < len(nums):
                if nums[right] == target:
                    return right
            return -1

        return [start(), end()]


sol = Solution()

# print(sol.searchRange([5, 7, 7, 8, 8, 10], 8))  # [3,4]

assert sol.searchRange([5, 7, 7, 8, 8, 10], 8) == [3, 4]
assert sol.searchRange([5, 7, 7, 8, 8, 10], 6) == [-1, -1]
assert sol.searchRange([], 0) == [-1, -1]
assert sol.searchRange([1], 1) == [0, 0]
assert sol.searchRange([1], 2) == [-1, -1]
assert sol.searchRange([2, 2, 2, 2], 2) == [0, 3]
assert sol.searchRange([1, 2, 3, 4], 3) == [2, 2]
assert sol.searchRange([1, 1, 2, 3], 1) == [0, 1]
assert sol.searchRange([1, 2, 3, 3], 3) == [2, 3]
assert sol.searchRange([1, 2, 3], 0) == [-1, -1]
assert sol.searchRange([1, 2, 3], 4) == [-1, -1]
assert sol.searchRange([-1, 0, 1], 0) == [1, 1]
assert sol.searchRange([-1, 0, 1], -2) == [-1, -1]
assert sol.searchRange([5, 7, 7, 8, 8, 10], 7) == [1, 2]
assert sol.searchRange([5, 7, 7, 8, 8, 10], 10) == [5, 5]
assert sol.searchRange([5, 7, 7, 8, 8, 10], 5) == [0, 0]
assert sol.searchRange([2, 2, 2], 3) == [-1, -1]
