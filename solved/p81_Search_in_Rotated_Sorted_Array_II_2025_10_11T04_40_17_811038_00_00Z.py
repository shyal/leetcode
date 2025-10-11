"""
URL: https://leetcode.com/problems/search-in-rotated-sorted-array-ii/description/

81. Search in Rotated Sorted Array II

There is an integer array nums sorted in non-decreasing order (not necessarily with distinct elements).

Before being passed to your function, nums is rotated at an unknown pivot index k (0 <= k < nums.length) such that the resulting array is [nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]] (0-indexed). For example, [0,1,2,4,4,4,5,6,6,7] might be rotated at pivot index 5 and become [4,5,6,6,7,0,1,2,4,4].

Given the array nums after the rotation and an integer target, return true if target is in nums, or false if it is not in nums.

You must decrease the overall operation steps as much as possible.


Example 1:

Input: nums = [2,5,6,0,0,1,2], target = 0
Output: true

Example 2:

Input: nums = [2,5,6,0,0,1,2], target = 3
Output: false


Constraints:

    1 <= nums.length <= 5000
    -10^4 <= nums[i] <= 10^4
    nums is guaranteed to be rotated at some pivot.
    -10^4 <= target <= 10^4


Follow up: This problem is similar to Search in Rotated Sorted Array, but nums may contain duplicates. Would this affect the runtime complexity? How and why?
"""


class Solution:
    def search(self, nums: List[int], target: int) -> bool:
        n = len(nums) - 1
        left, right = 0, n
        result = -1
        while left <= right:
            mid = left + (right - left) // 2
            left_is_sorted = nums[left] <= nums[mid]
            right_is_sorted = not left_is_sorted

            if nums[mid] == target:
                return True
            elif left_is_sorted:
                if nums[left] == nums[mid]:
                    left += 1
                elif nums[left] <= target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            elif right_is_sorted:
                if nums[mid] == nums[right]:
                    right -= 1
                elif nums[mid] < target <= nums[right]:
                    left = mid + 1
                else:
                    right = mid - 1
        return False


sol = Solution()

# print(sol.search([2, 5, 6, 0, 0, 1, 2], 0))  # True

assert sol.search([2, 5, 6, 0, 0, 1, 2], 0) == True
assert sol.search([2, 5, 6, 0, 0, 1, 2], 3) == False
assert sol.search([1], 1) == True
assert sol.search([1], 2) == False
assert sol.search([2, 1], 2) == True
assert sol.search([2, 1], 1) == True
assert sol.search([2, 1], 3) == False
assert sol.search([5, 5, 5, 5, 5], 5) == True
assert sol.search([5, 5, 5, 5, 5], 6) == False
assert sol.search([1, 3, 1, 1, 1], 3) == True
assert sol.search([1, 3, 1, 1, 1], 1) == True
assert sol.search([1, 3, 1, 1, 1], 0) == False
assert sol.search([3, 1, 1, 1, 1, 1, 1, 1], 3) == True
assert sol.search([3, 1, 1, 1, 1, 1, 1, 1], 2) == False
assert sol.search([1, -1], -1) == True
assert sol.search([1, -1], 0) == False
assert sol.search([4, 5, 6, 7, 0, 1, 2], -1) == False
assert sol.search([4, 5, 6, 7, 0, 1, 2], 0) == True
assert sol.search([1, 1, 1, 1, 1, 1, 1], 1) == True
assert sol.search([1, 1, 1, 1, 1, 1, 1], 2) == False
assert sol.search([1, 1, 1, 1, 1, 1, 1, 1], 1) == True
assert sol.search([1, 1, 1, 1, 1, 1, 1, 1], 0) == False
assert sol.search([10000, -10000], 10000) == True
assert sol.search([10000, -10000], -10000) == True
assert sol.search([10000, -10000], 0) == False
assert sol.search([1, 1, 1, 2, 1, 1, 1], 2) == True
assert sol.search([1, 1, 1, 2, 1, 1, 1], 3) == False
assert sol.search([2, 2, 2, 3, 2, 2, 2], 3) == True
assert sol.search([2, 2, 2, 3, 2, 2, 2], 1) == False
assert sol.search([1, 1, 1, 1, 1, 2, 1], 2) == True
assert sol.search([1, 1, 1, 1, 1, 2, 1], 3) == False
assert sol.search([5000, 5000, 5000, 1, 5000, 5000], 1) == True
assert sol.search([5000, 5000, 5000, 1, 5000, 5000], 2) == False
assert sol.search([1, 2, 3, 4, 5, 6, 7, 8], 8) == True
assert sol.search([1, 2, 3, 4, 5, 6, 7, 8], 0) == False
assert sol.search([2, 3, 4, 5, 6, 7, 8, 1], 1) == True
assert sol.search([2, 3, 4, 5, 6, 7, 8, 1], 9) == False
assert sol.search([1, 1, 1, 1, 2, 1, 1, 1], 2) == True
assert sol.search([1, 1, 1, 1, 2, 1, 1, 1], 3) == False
assert sol.search([3, 3, 3, 1, 2, 3, 3, 3], 2) == True
assert sol.search([3, 3, 3, 1, 2, 3, 3, 3], 4) == False
