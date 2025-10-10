"""
URL: https://leetcode.com/problems/search-in-rotated-sorted-array/description/

33. Search in Rotated Sorted Array

There is an integer array nums sorted in ascending order (with distinct values).

Prior to being passed to your function, nums is possibly rotated at an unknown pivot index k (1 <= k < nums.length) such that the resulting array is [nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]] (0-based index). Given the array nums after the possible rotation and an integer target, return the index of target if it is in nums, or -1 if it is not in nums.

You must write an algorithm with O(log n) runtime complexity.

Example 1:

Input: nums = [4,5,6,7,0,1,2], target = 0
Output: 4

Example 2:

Input: nums = [4,5,6,7,0,1,2], target = 3
Output: -1

Example 3:

Input: nums = [1], target = 0
Output: -1

Constraints:

    1 <= nums.length <= 5000
    -10^4 <= nums[i] <= 10^4
    All values of nums are unique.
    nums is guaranteed to be rotated at some pivot.
    -10^4 <= target <= 10^4

---

This question is my archnemesis for some reason. I got close, but had to
look up the solution in the end.

I don't know why. It's really not that hard. We can only search in sorted arrays
so if the left is sorted, our first decision is to branch into the left
search conditional, then if it's in the left, the next iteration will
search in this sublist, else it'll search the other.

Vice versa with the right side. I keep encountering this question, and
forgetting.

Will need to revisit soon.

"""


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums) - 1

        while left <= right:
            mid = (left + right) // 2

            if nums[mid] == target:
                return mid

            left_is_sorted = nums[left] <= nums[mid]
            right_is_sorted = not left_is_sorted

            if left_is_sorted:
                target_is_in_left = nums[left] <= target < nums[mid]
                if target_is_in_left:
                    right = mid - 1
                else:
                    left = mid + 1
            elif right_is_sorted:
                target_is_in_right = nums[mid] < target <= nums[right]
                if target_is_in_right:
                    left = mid + 1
                else:
                    right = mid - 1

        return -1


sol = Solution()

# print(sol.search([4, 5, 6, 7, 0, 1, 2], 0))  # 4

assert sol.search([4, 5, 6, 7, 0, 1, 2], 0) == 4
assert sol.search([4, 5, 6, 7, 0, 1, 2], 3) == -1
assert sol.search([1], 0) == -1
assert sol.search([1], 1) == 0
assert sol.search([4, 5, 6, 7, 0, 1, 2], 4) == 0
assert sol.search([4, 5, 6, 7, 0, 1, 2], 2) == 6
assert sol.search([4, 5, 6, 7, 0, 1, 2], 7) == 3
assert sol.search([2, 1], 2) == 0
assert sol.search([2, 1], 1) == 1
assert sol.search([2, 1], 3) == -1
assert sol.search([1, 2, 3, 4, 5, 6, 0], 0) == 6
assert sol.search([1, 2, 3, 4, 5, 6, 0], 1) == 0
assert sol.search([1, 2, 3, 4, 5, 6, 0], 4) == 3
assert sol.search([1, 2, 3, 4, 5, 6, 0], 7) == -1
assert sol.search([2, 4, -5, -3, 0], -5) == 2
assert sol.search([2, 4, -5, -3, 0], 4) == 1
assert sol.search([2, 4, -5, -3, 0], 0) == 4
assert sol.search([2, 4, -5, -3, 0], 3) == -1
assert sol.search([2, 4, -5, -3, 0], -6) == -1
assert sol.search([-3, -1, -5, -4], -5) == 2
assert sol.search([-3, -1, -5, -4], -4) == 3
assert sol.search([-3, -1, -5, -4], -3) == 0
assert sol.search([-3, -1, -5, -4], 0) == -1
