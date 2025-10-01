"""
https://leetcode.com/problems/find-pivot-index/description

724. Find Pivot Index
Easy
Given an array of integers nums, calculate the pivot index of this array.

The pivot index is the index where the sum of all the numbers strictly to the left of the index is equal to the sum of all the numbers strictly to the index's right.

If the index is on the left edge of the array, then the left sum is 0 because there are no elements to the left. This also applies to the right edge of the array.

Return the leftmost pivot index. If no such index exists, return -1.
 

Example 1:

Input: nums = [1,7,3,6,5,6]
Output: 3
Explanation:
The pivot index is 3.
Left sum = nums[0] + nums[1] + nums[2] = 1 + 7 + 3 = 11
Right sum = nums[4] + nums[5] = 5 + 6 = 11
Example 2:

Input: nums = [1,2,3]
Output: -1
Explanation:
There is no index that satisfies the conditions in the problem statement.
Example 3:

Input: nums = [2,1,-1]
Output: 0
Explanation:
The pivot index is 0.
Left sum = 0 (no elements to the left of index 0)
Right sum = nums[1] + nums[2] = 1 + -1 = 0
 

Constraints:

1 <= nums.length <= 104
-1000 <= nums[i] <= 1000
 

Note: This question is the same as 1991: https://leetcode.com/problems/find-the-middle-index-in-array/
"""


class Solution:
    def pivotIndex(self, nums: List[int]) -> int:
        total = sum(nums)
        prefix_sum = 0
        for i, n in enumerate(nums):
            total -= n
            if prefix_sum == total:
                return i
            prefix_sum += n
        return -1


sol = Solution()

assert sol.pivotIndex([1, 7, 3, 6, 5, 6]) == 3
assert sol.pivotIndex([1, 2, 3]) == -1
assert sol.pivotIndex([2, 1, -1]) == 0
assert sol.pivotIndex([5]) == 0
assert sol.pivotIndex([1, -1]) == -1
assert sol.pivotIndex([0, 0, 0]) == 0
assert sol.pivotIndex([-1, -1, 0, 1, 1, 0]) == 5
assert sol.pivotIndex([1000, -1000, 0]) == 2
assert sol.pivotIndex([10, 20, 30, 40]) == -1
assert sol.pivotIndex([0, 0, 0, 0]) == 0
assert sol.pivotIndex([-2, -1, -1, -2, -6]) == -1
assert sol.pivotIndex([1, 2, 3, 4, 6]) == 3

