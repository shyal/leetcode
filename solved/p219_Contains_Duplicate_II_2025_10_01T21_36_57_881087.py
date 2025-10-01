"""
URL: https://leetcode.com/problems/contains-duplicate-ii/description/

219. Contains Duplicate II

Given an integer array nums and an integer k, return true if there are two distinct indices i and j in the array such that nums[i] == nums[j] and abs(i - j) <= k.


Example 1:

Input: nums = [1,2,3,1], k = 3
Output: true

Example 2:

Input: nums = [1,0,1,1], k = 1
Output: true

Example 3:

Input: nums = [1,2,3,1,2,3], k = 2
Output: false


Constraints:

        1 <= nums.length <= 105
        -109 <= nums[i] <= 109
        0 <= k <= 105
"""


class Solution:
    def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
        nums = [*enumerate(nums)]
        nums.sort(key=lambda x: x[1])
        for i in range(1, len(nums)):
            if nums[i][1] == nums[i - 1][1] and abs(nums[i][0] - nums[i - 1][0]) <= k:
                return True
        return False


sol = Solution()

assert sol.containsNearbyDuplicate([1, 2, 3, 1], 3) == True
assert sol.containsNearbyDuplicate([1, 0, 1, 1], 1) == True
assert sol.containsNearbyDuplicate([1, 2, 3, 1, 2, 3], 2) == False
assert sol.containsNearbyDuplicate(range(-30000, 30000), 35000) == False
