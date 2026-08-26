"""
URL: https://leetcode.com/problems/two-sum/description/?envType=problem-list-v2&envId=vn57k9wr

1. Two Sum

You are given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.

Example 1:

Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].

Example 2:

Input: nums = [3,2,4], target = 6
Output: [1,2]

Example 3:

Input: nums = [3,3], target = 6
Output: [0,1]

Constraints:

    2 <= nums.length <= 10^4
    -10^9 <= nums[i] <= 10^9
    -10^9 <= target <= 10^9
    Only one valid answer exists.

Follow-up: Can you come up with an algorithm that is less than O(n^2) time complexity?
"""


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        D = {}
        for i, n in enumerate(nums):
            if n in D:
                return [D[n], i]
            D[target - n] = i


sol = Solution()

print(sol.twoSum([2, 7, 11, 15], 9))  # [0,1]

assert sol.twoSum([2, 7, 11, 15], 9) == [0, 1]
assert sol.twoSum([3, 2, 4], 6) == [1, 2]
assert sol.twoSum([3, 3], 6) == [0, 1]

assert sol.twoSum([1, 1], 2) == [0, 1]
assert sol.twoSum([-1, -2, -3, -4, -5], -8) == [2, 4]
assert sol.twoSum([0, 0], 0) == [0, 1]
assert sol.twoSum([10**9, -(10**9), 0, 1], 1) == [2, 3]
assert sol.twoSum([5, 5, 5, 5], 10) == [0, 1]
assert sol.twoSum([1, 2], 3) == [0, 1]
assert sol.twoSum([2, 5, 5, 11], 10) == [1, 2]
assert sol.twoSum([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 19) == [8, 9]
assert sol.twoSum([-(10**9), 10**9], 0) == [0, 1]
assert sol.twoSum([0, 1, 2, 3, 4, 5, 6, 7, 8, 9] * 1000, 17) == [8, 9]
assert sol.twoSum([2, 7, 11, 15], 26) == [2, 3]
assert sol.twoSum([1, 3, 3, 4], 6) == [1, 2]
