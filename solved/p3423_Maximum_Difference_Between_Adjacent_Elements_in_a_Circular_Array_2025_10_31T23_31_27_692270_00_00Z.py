"""
URL: https://leetcode.com/problems/maximum-difference-between-adjacent-elements-in-a-circular-array/description/?envType=problem-list-v2&envId=vn57k9wr

3423. Maximum Difference Between Adjacent Elements in a Circular Array

Given a circular array nums, find the maximum absolute difference between adjacent elements.

Note: In a circular array, the first and last elements are adjacent.


Example 1:

Input: nums = [1,2,4]
Output: 3
Explanation:
Because nums is circular, nums[0] and nums[2] are adjacent. They have the maximum absolute difference of |4 - 1| = 3.

Example 2:

Input: nums = [-5,-10,-5]
Output: 5
Explanation:
The adjacent elements nums[0] and nums[1] have the maximum absolute difference of |-5 - (-10)| = 5.


Constraints:

    2 <= nums.length <= 100
    -100 <= nums[i] <= 100
"""


class Solution:
    def maxAdjacentDistance(self, nums: List[int]) -> int:
        return max([abs(a - b) for a, b in pairwise(nums)] + [abs(nums[0] - nums[-1])])


sol = Solution()

# print(sol.maxAdjacentDistance([1, 2, 4]))  # 3

assert sol.maxAdjacentDistance([1, 2, 4]) == 3
assert sol.maxAdjacentDistance([-5, -10, -5]) == 5
assert sol.maxAdjacentDistance([1, 1]) == 0
assert sol.maxAdjacentDistance([100, -100]) == 200
assert sol.maxAdjacentDistance([-100, 100, -100]) == 200
assert sol.maxAdjacentDistance([1, 2, 3, 4, 5]) == 4
assert sol.maxAdjacentDistance([5, 4, 3, 2, 1]) == 4
assert sol.maxAdjacentDistance([0, 0, 0]) == 0
assert sol.maxAdjacentDistance([-1, -2, -3]) == 2
assert sol.maxAdjacentDistance([99, 100, -100, 50]) == 200
assert sol.maxAdjacentDistance([1, 3, 2]) == 2
assert sol.maxAdjacentDistance([-100, -100, -100, -100]) == 0
assert sol.maxAdjacentDistance([100, 0, -100]) == 200
