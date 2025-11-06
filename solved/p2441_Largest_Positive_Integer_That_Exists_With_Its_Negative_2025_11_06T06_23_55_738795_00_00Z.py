"""
URL: https://leetcode.com/problems/largest-positive-integer-that-exists-with-its-negative/description/?envType=problem-list-v2&envId=vn57k9wr

2441. Largest Positive Integer That Exists With Its Negative

Given an integer array nums that does not contain any zeros, find the largest positive integer k such that -k also exists in the array.

Return the positive integer k. If there is no such integer, return -1.

Example 1:

Input: nums = [-1,2,-3,3]
Output: 3
Explanation: 3 is the only valid k we can find in the array.

Example 2:

Input: nums = [-1,10,6,7,-7,1]
Output: 7
Explanation: Both 1 and 7 have their corresponding negative values in the array. 7 has a larger value.

Example 3:

Input: nums = [-10,8,6,7,-2,-3]
Output: -1
Explanation: There is no a single valid k, we return -1.

Constraints:

    1 <= nums.length <= 1000
    -1000 <= nums[i] <= 1000
    nums[i] != 0
"""


class Solution:
    def findMaxK(self, nums: List[int]) -> int:
        _max = 0
        nums = set(nums)
        for n in nums:
            if -n in nums:
                _max = max(_max, n)
        return _max or -1


sol = Solution()

# print(sol.findMaxK([-1, 2, -3, 3]))  # 3

assert sol.findMaxK([-1, 2, -3, 3]) == 3
assert sol.findMaxK([-1, 10, 6, 7, -7, 1]) == 7
assert sol.findMaxK([-10, 8, 6, 7, -2, -3]) == -1
assert sol.findMaxK([5]) == -1
assert sol.findMaxK([-5]) == -1
assert sol.findMaxK([1, -1]) == 1
assert sol.findMaxK([1000, -1000]) == 1000
assert sol.findMaxK([1, 2, 3, -1, -2, -3]) == 3
assert sol.findMaxK([1, 2, 3, -4]) == -1
assert sol.findMaxK([10, -5, 5]) == 5
assert sol.findMaxK([-1, -2, -3]) == -1
assert sol.findMaxK([1, 2, 3]) == -1
assert sol.findMaxK([1, 1, -1, -1]) == 1
assert sol.findMaxK([-1, 1, -2, 2, -3, 3, 4]) == 3
assert sol.findMaxK([1000, 999, -1000]) == 1000
assert sol.findMaxK([1, -1, -2]) == 1
assert sol.findMaxK([2, -2]) == 2
