"""
URL: https://leetcode.com/problems/search-insert-position/description/

35. Search Insert Position

Given a sorted array of distinct integers and a target value, return the index if the target is found. If not, return the index where it would be if it were inserted in order.
You may assume no duplicates in the array.


Example 1:

Input: nums = [1,3,5,6], target = 5
Output: 2

Example 2:

Input: nums = [1,3,5,6], target = 2
Output: 1

Example 3:

Input: nums = [1,3,5,6], target = 7
Output: 4


Constraints:

    1 <= nums.length <= 104
    -104 <= nums[i] <= 104
    nums contains distinct values sorted in ascending order.
    -104 <= target <= 104

"""


class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        return bisect_left(nums, target)


sol = Solution()

# print(sol.searchInsert([1, 3, 5, 6], 5))  # 2

assert sol.searchInsert([1, 3, 5, 6], 5) == 2
assert sol.searchInsert([1, 3, 5, 6], 2) == 1
assert sol.searchInsert([1, 3, 5, 6], 7) == 4
assert sol.searchInsert([1], 1) == 0
assert sol.searchInsert([1], 0) == 0
assert sol.searchInsert([1], 2) == 1
assert sol.searchInsert([1, 3, 5, 6], 0) == 0
assert sol.searchInsert([1, 3, 5, 6], 6) == 3
assert sol.searchInsert([1, 3, 5, 6], 1) == 0
assert sol.searchInsert([-5, -3, -1], -4) == 1
assert sol.searchInsert([-5, -3, -1], -6) == 0
assert sol.searchInsert([-5, -3, -1], 0) == 3
assert sol.searchInsert([1, 2, 3, 4, 5], 3) == 2
assert sol.searchInsert([1, 2, 4, 5], 3) == 2
assert sol.searchInsert([-10, -5, 0, 5, 10], -15) == 0
assert sol.searchInsert([-10, -5, 0, 5, 10], 15) == 5
assert sol.searchInsert([-10, -5, 0, 5, 10], 0) == 2
