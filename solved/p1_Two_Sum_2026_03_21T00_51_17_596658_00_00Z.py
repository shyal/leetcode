"""
URL: https://leetcode.com/problems/two-sum/description/?envType=problem-list-v2&envId=vn57k9wr

1. Two Sum

Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

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
"""

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        s = dd(int)
        for i, n in enumerate(nums):
            k = target - n
            if k in s:
                return [s[k], i]
            s[n] = i

sol = Solution()

print(sol.twoSum([2,7,11,15], 9))  # [0,1]

assert sol.twoSum([2,7,11,15], 9) == [0,1]
assert sol.twoSum([3,2,4], 6) == [1,2]
assert sol.twoSum([3,3], 6) == [0,1]
assert sol.twoSum([-1,1], 0) == [0,1]
assert sol.twoSum([0,0], 0) == [0,1]
assert sol.twoSum([-1000000000,1000000000], 0) == [0,1]
assert sol.twoSum([1,3,5,7], 10) == [1,3]
assert sol.twoSum([-5,-4], -9) == [0,1]
assert sol.twoSum([2,1,5,3], 4) == [1,3]
# assert sol.twoSum([3,2,3], 5) == [1,2]
assert sol.twoSum([-3,1,2,5], -1) == [0,2]