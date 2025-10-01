"""
URL: https://leetcode.com/problems/house-robber/description/?envType=study-plan-v2&envId=leetcode-75

198. House Robber

You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed, the only constraint stopping you from robbing each of them is that adjacent houses have security systems connected and it will automatically contact the police if two adjacent houses were broken into on the same night.

Given an integer array nums representing the amount of money of each house, return the maximum amount of money you can rob tonight without alerting the police.


Example 1:

Input: nums = [1,2,3,1]
Output: 4
Explanation: Rob house 1 (money = 1) and then rob house 3 (money = 3).
Total amount you can rob = 1 + 3 = 4.

Example 2:

Input: nums = [2,7,9,3,1]
Output: 12
Explanation: Rob house 1 (money = 2), rob house 3 (money = 9) and rob house 5 (money = 1).
Total amount you can rob = 2 + 9 + 1 = 12.


Constraints:

        1 <= nums.length <= 100
        0 <= nums[i] <= 400
"""

"""

Let's think of more examples

Example 2:

Input: nums = [1, 1, 5, 5, 5, 6]

"""

from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        _max = 0
        for i in range(len(nums) - 1, -1, -1):
            v = nums[i]
            nums[i] = max(
                (v + nums[i + 2]) if i + 2 < len(nums) else v,
                (v + nums[i + 3]) if i + 3 < len(nums) else v,
            )
            _max = max(nums[i], _max)
        return _max


sol = Solution()

res = sol.rob(nums=[1, 5, 1, 5, 1, 1, 8, 1, 1])
assert res == 19

res = sol.rob(nums=[1, 2, 3, 1])
assert res == 4

res = sol.rob(nums=[2, 7, 9, 3, 1])
assert res == 12

res = sol.rob(nums=[1, 1, 5, 5, 5, 6])
assert res == 12

res = sol.rob(nums=[1])
assert res == 1

res = sol.rob(nums=[0])
assert res == 0

res = sol.rob(nums=[1, 2])
assert res == 2

res = sol.rob(nums=[2, 1])
assert res == 2

res = sol.rob(nums=[0, 0])
assert res == 0

res = sol.rob(nums=[1, 0])
assert res == 1

res = sol.rob(nums=[0, 1])
assert res == 1

res = sol.rob(nums=[1, 3, 1])
assert res == 3

res = sol.rob(nums=[4, 1, 1, 4])
assert res == 8

res = sol.rob(nums=[1, 2, 3, 4, 5])
assert res == 9

res = sol.rob(nums=[10, 1, 10, 1, 10])
assert res == 30

res = sol.rob(nums=[1, 10, 1, 10, 1])
assert res == 20

res = sol.rob(nums=[0, 0, 0, 0])
assert res == 0

res = sol.rob(nums=[400, 400, 400])
assert res == 800

res = sol.rob(nums=[2, 3, 2])
assert res == 4

res = sol.rob(nums=[5])
assert res == 5

res = sol.rob(nums=[0, 0, 5])
assert res == 5

res = sol.rob(nums=[100, 0, 0, 100])
assert res == 200

res = sol.rob(nums=[1, 2, 3, 1, 1, 3])
assert res == 7
