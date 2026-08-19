"""
URL: https://leetcode.com/problems/binary-search/description/?envType=problem-list-v2&envId=vn57k9wr

704. Binary Search

Given an array of integers nums which is sorted in ascending order, and an
integer target, write a function to search target in nums. If target exists,
then return its index. Otherwise, return -1.

You must write an algorithm with O(log n) runtime complexity.


Example 1:

Input: nums = [-1,0,3,5,9,12], target = 9
Output: 4
Explanation: 9 exists in nums and its index is 4

Example 2:

Input: nums = [-1,0,3,5,9,12], target = 2
Output: -1
Explanation: 2 does not exist in nums so return -1


Constraints:

    1 <= nums.length <= 10^4
    -10^4 < nums[i], target < 10^4
    All the integers in nums are unique.
    nums is sorted in ascending order.
"""


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums) -1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1


sol = Solution()

print(sol.search([-1, 0, 3, 5, 9, 12], 9))  # 4

assert sol.search([-1, 0, 3, 5, 9, 12], 9) == 4
assert sol.search([-1, 0, 3, 5, 9, 12], 2) == -1
assert sol.search([-1, 0, 3, 5, 9, 12], -1) == 0
assert sol.search([-1, 0, 3, 5, 9, 12], 12) == 5
assert sol.search([-1, 0, 3, 5, 9, 12], 5) == 3
assert sol.search([-1, 0, 3, 5, 9, 12], 3) == 2
assert sol.search([-1, 0, 3, 5, 9, 12], -5) == -1
assert sol.search([-1, 0, 3, 5, 9, 12], 13) == -1
assert sol.search([-1, 0, 3, 5, 9, 12], 10) == -1
assert sol.search([5], 5) == 0
assert sol.search([5], -5) == -1
assert sol.search([5], 7) == -1
assert sol.search([2, 5], 2) == 0
assert sol.search([2, 5], 5) == 1
assert sol.search([2, 5], 0) == -1
assert sol.search([2, 5], 3) == -1
assert sol.search([2, 5], 9) == -1
assert sol.search([-4, -2, 0, 2, 4], 0) == 2
assert sol.search([-4, -2, 0, 2, 4], -4) == 0
assert sol.search([-4, -2, 0, 2, 4], 4) == 4
assert sol.search([-4, -2, 0, 2, 4], 1) == -1
assert sol.search(list(range(100)), 0) == 0
assert sol.search(list(range(100)), 99) == 99
assert sol.search(list(range(100)), 37) == 37
assert sol.search(list(range(100)), 100) == -1
assert sol.search(list(range(100)), -1) == -1