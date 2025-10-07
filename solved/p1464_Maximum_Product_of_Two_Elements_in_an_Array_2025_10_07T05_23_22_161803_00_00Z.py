"""
URL: https://leetcode.com/problems/maximum-product-of-two-elements-in-an-array/description/

1464. Maximum Product of Two Elements in an Array

Given the array of integers nums, you will choose two different indices i and j of that array. Return the maximum value of (nums[i]-1)*(nums[j]-1).


Example 1:

Input: nums = [3,4,5,2]
Output: 12
Explanation: If you choose the indices i=1 and j=2 (indexed from 0), you will get the maximum value, that is, (nums[1]-1)*(nums[2]-1) = (4-1)*(5-1) = 3*4 = 12.

Example 2:

Input: nums = [1,5,4,5]
Output: 16
Explanation: Choosing the indices i=1 and j=3 (indexed from 0), you will get (5-1)*(5-1) = 16.

Example 3:

Input: nums = [3,7]
Output: 12


Constraints:

    2 <= nums.length <= 500
    1 <= nums[i] <= 10^3
"""


class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        return max(
            (nums[i] - 1) * (nums[j] - 1) for i, j in combinations(range(len(nums)), 2)
        )


sol = Solution()

# print(sol.maxProduct([3, 4, 5, 2]))  # 12

assert sol.maxProduct([3, 4, 5, 2]) == 12
assert sol.maxProduct([1, 5, 4, 5]) == 16
assert sol.maxProduct([3, 7]) == 12
assert sol.maxProduct([1, 1]) == 0
assert sol.maxProduct([1000, 1000]) == 998001
assert sol.maxProduct([1, 1000]) == 0
assert sol.maxProduct([2, 3, 4, 5, 6]) == 20
assert sol.maxProduct([5, 5, 5, 5]) == 16
assert sol.maxProduct([1, 2, 3]) == 2
