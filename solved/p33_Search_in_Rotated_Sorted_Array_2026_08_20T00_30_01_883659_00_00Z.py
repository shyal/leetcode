"""
URL: https://leetcode.com/problems/search-in-rotated-sorted-array/description/?envType=problem-list-v2&envId=vn57k9wr

33. Search in Rotated Sorted Array

There is an integer array nums sorted in ascending order (with distinct values).

Prior to being passed to your function, nums is possibly left rotated at an
unknown index k (1 <= k < nums.length) such that the resulting array is
[nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]]
(0-indexed). For example, [0,1,2,4,5,6,7] might be left rotated by 3 indices
and become [4,5,6,7,0,1,2].

Given the array nums after the possible rotation and an integer target,
return the index of target if it is in nums, or -1 if it is not in nums.

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
    nums is an ascending array that is possibly rotated.
    -10^4 <= target <= 10^4

---


       m
 l
[4,5,6,7,0,1,2]
             r

       m
 l
[6,7,0,1,2,4,5]
             r

"""

class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums) -1
        while left <= right:
            mid = (left + right) // 2
            mid_val = nums[mid]
            left_val = nums[left]
            right_val = nums[right]
            left_is_sorted = left_val <= mid_val
            if mid_val == target:
                return mid
            elif left_is_sorted:
                if left_val <= target <= mid_val:
                    right = mid - 1
                else:
                    left = mid + 1
            else:
                if mid_val <= target <= right_val:
                    left = mid + 1
                else:
                    right = mid -1
        return -1
        
            


sol = Solution()

# print(sol.search([4, 5, 6, 7, 0, 1, 2], 0))  # 4

assert sol.search([4, 5, 6, 7, 0, 1, 2], 0) == 4
assert sol.search([4, 5, 6, 7, 0, 1, 2], 3) == -1
assert sol.search([1], 0) == -1
assert sol.search([1], 1) == 0
assert sol.search([4, 5, 6, 7, 0, 1, 2], 4) == 0
assert sol.search([4, 5, 6, 7, 0, 1, 2], 7) == 3
assert sol.search([4, 5, 6, 7, 0, 1, 2], 2) == 6
assert sol.search([4, 5, 6, 7, 0, 1, 2], 5) == 1
assert sol.search([4, 5, 6, 7, 0, 1, 2], 1) == 5
assert sol.search([4, 5, 6, 7, 0, 1, 2], -1) == -1
assert sol.search([4, 5, 6, 7, 0, 1, 2], 8) == -1
assert sol.search([1, 3], 1) == 0
assert sol.search([1, 3], 3) == 1
assert sol.search([3, 1], 3) == 0
assert sol.search([3, 1], 1) == 1
assert sol.search([3, 1], 2) == -1
assert sol.search([5, 1, 3], 5) == 0
assert sol.search([5, 1, 3], 1) == 1
assert sol.search([5, 1, 3], 3) == 2
assert sol.search([5, 1, 3], 2) == -1
assert sol.search([5, 1, 3], 4) == -1
assert sol.search([1, 2, 3, 4, 5], 1) == 0
assert sol.search([1, 2, 3, 4, 5], 3) == 2
assert sol.search([1, 2, 3, 4, 5], 5) == 4
assert sol.search([1, 2, 3, 4, 5], 0) == -1
assert sol.search([1, 2, 3, 4, 5], 6) == -1
assert sol.search([2, 3, 4, 5, 1], 1) == 4
assert sol.search([2, 3, 4, 5, 1], 2) == 0
assert sol.search([9, 12, -1, 0, 3, 5], -1) == 2
assert sol.search([9, 12, -1, 0, 3, 5], 12) == 1
assert sol.search([9, 12, -1, 0, 3, 5], 9) == 0
assert sol.search([9, 12, -1, 0, 3, 5], 5) == 5
assert sol.search([9, 12, -1, 0, 3, 5], 7) == -1
assert sol.search([6, 7, 8, 1, 2, 3, 4, 5], 8) == 2
assert sol.search([6, 7, 8, 1, 2, 3, 4, 5], 6) == 0
assert sol.search([6, 7, 8, 1, 2, 3, 4, 5], 5) == 7
assert sol.search([6, 7, 8, 1, 2, 3, 4, 5], 1) == 3
assert sol.search([6, 7, 8, 1, 2, 3, 4, 5], 0) == -1
assert sol.search([-10000, 10000], 10000) == 1
assert sol.search([10000, -10000], -10000) == 1