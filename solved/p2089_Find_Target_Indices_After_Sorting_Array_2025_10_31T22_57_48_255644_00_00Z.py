"""
URL: https://leetcode.com/problems/find-target-indices-after-sorting-array/description/?envType=problem-list-v2&envId=vn57k9wr

2089. Find Target Indices After Sorting Array

You are given a 0-indexed integer array nums and a target element target.

A target index is an index i such that nums[i] == target.

Return a list of the target indices of nums after sorting nums in non-decreasing order. If there are no target indices, return an empty list. The returned list must be sorted in increasing order.


Example 1:

Input: nums = [1,2,5,2,3], target = 2
Output: [1,2]
Explanation: After sorting, nums is [1,2,2,3,5].
The indices where nums[i] == 2 are 1 and 2.

Example 2:

Input: nums = [1,2,5,2,3], target = 3
Output: [3]
Explanation: After sorting, nums is [1,2,2,3,5].
The index where nums[i] == 3 is 3.

Example 3:

Input: nums = [1,2,5,2,3], target = 5
Output: [4]
Explanation: After sorting, nums is [1,2,2,3,5].
The index where nums[i] == 5 is 4.


Constraints:

    1 <= nums.length <= 100
    1 <= nums[i], target <= 100
"""


class Solution:
    def targetIndices(self, nums: List[int], target: int) -> List[int]:
        nums.sort()
        return [i for i, v in enumerate(nums) if v == target]


sol = Solution()

# print(sol.targetIndices([1, 2, 5, 2, 3], 2))  # [1,2]

assert sol.targetIndices([1, 2, 5, 2, 3], 2) == [1, 2]
assert sol.targetIndices([1, 2, 5, 2, 3], 3) == [3]
assert sol.targetIndices([1, 2, 5, 2, 3], 5) == [4]
assert sol.targetIndices([1], 1) == [0]
assert sol.targetIndices([1], 2) == []
assert sol.targetIndices([2, 2, 2], 2) == [0, 1, 2]
assert sol.targetIndices([1, 3, 2, 4], 5) == []
assert sol.targetIndices([5, 4, 3, 2], 1) == []
assert sol.targetIndices([100, 99, 98], 99) == [1]
assert sol.targetIndices([1, 2, 2, 3, 3, 3, 4], 3) == [3, 4, 5]
assert sol.targetIndices([1, 1, 2, 2, 3, 3], 4) == []
