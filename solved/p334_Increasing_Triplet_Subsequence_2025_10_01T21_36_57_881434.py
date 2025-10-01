"""
URL: https://leetcode.com/problems/increasing-triplet-subsequence/description/?envType=study-plan-v2&envId=leetcode-75

334. Increasing Triplet Subsequence

Given an integer array nums, return true if there exists a triple of indices (i, j, k) such that i < j < k and nums[i] < nums[j] < nums[k]. If no such indices exists, return false.


Example 1:

Input: nums = [1,2,3,4,5]
Output: true
Explanation: Any triplet where i < j < k is valid.

Example 2:

Input: nums = [5,4,3,2,1]
Output: false
Explanation: No triplet exists.

Example 3:

Input: nums = [2,1,5,0,4,6]
Output: true
Explanation: One of the valid triplet is (3, 4, 5), because nums[3] == 0 < nums[4] == 4 < nums[5] == 6.


Constraints:

        1 <= nums.length <= 5 * 105
        -231 <= nums[i] <= 231 - 1


Follow up: Could you implement a solution that runs in O(n) time complexity and O(1) space complexity?
"""

from typing import List


class Solution:
    def increasingTriplet(self, nums: List[int]) -> bool:
        a = float("inf")
        b = float("inf")

        for n in nums:
            if n <= a:
                a = n
            elif n <= b:
                b = n
            else:
                return True

        return False


sol = Solution()
assert sol.increasingTriplet(nums=[1, 2, 3, 4, 5]) == True
assert sol.increasingTriplet(nums=[5, 4, 3, 2, 1]) == False
assert sol.increasingTriplet(nums=[1, 2, 3]) == True
assert sol.increasingTriplet(nums=[3, 2, 1]) == False
assert sol.increasingTriplet(nums=[1, 1, 1]) == False
assert sol.increasingTriplet(nums=[1, 3, 2]) == False
assert sol.increasingTriplet(nums=[20, 100, 10, 12, 5, 13]) == True
assert sol.increasingTriplet(nums=[1, 5, 0, 4, 1, 3]) == True
assert sol.increasingTriplet(nums=[-1, -2, -3]) == False
assert sol.increasingTriplet(nums=[-5, -4, -3]) == True
assert sol.increasingTriplet(nums=[2, 2, 2]) == False
assert sol.increasingTriplet(nums=[1, 2, 2, 3]) == True
assert sol.increasingTriplet(nums=[5]) == False
assert sol.increasingTriplet(nums=[1, 2]) == False
assert sol.increasingTriplet(nums=[4, 5, 2147483647]) == True
assert sol.increasingTriplet(nums=[1, 0, 2, -1, 3]) == True
assert sol.increasingTriplet(nums=[6, 7, 1, 2]) == False
assert sol.increasingTriplet(nums=[1, 2, 1, 3]) == True
assert sol.increasingTriplet(nums=[0]) == False
assert sol.increasingTriplet(nums=[10, 9, 8, 7, 6, 5, 4, 3, 2, 1]) == False
assert sol.increasingTriplet(nums=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) == True
assert sol.increasingTriplet(nums=[2, 4, 1, 3, 5]) == True
