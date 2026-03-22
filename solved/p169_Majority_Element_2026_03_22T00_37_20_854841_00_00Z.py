"""
URL: https://leetcode.com/problems/majority-element/description/?envType=problem-list-v2&envId=vn57k9wr

169. Majority Element

Given an array nums of size n, return the majority element.

The majority element is the element that appears more than ⌊n / 2⌋ times. You may assume that the majority element always exists in the array.

Example 1:

Input: nums = [3,2,3]
Output: 3

Example 2:

Input: nums = [2,2,1,1,1,2,2]
Output: 2

Constraints:

- n == nums.length
- 1 <= n <= 5 * 10^4
- -10^9 <= nums[i] <= 10^9
- The input is generated such that a majority element will exist in the array.
"""

class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        c = Counter(nums).items()
        return max(c, key=lambda x: x[1])[0]

sol = Solution()

# print(sol.majorityElement([3,2,3]))  # 3

assert sol.majorityElement([3,2,3]) == 3
assert sol.majorityElement([2,2,1,1,1,2,2]) == 2
assert sol.majorityElement([1]) == 1
assert sol.majorityElement([2,2]) == 2
assert sol.majorityElement([-3,-3,-3,1,1]) == -3
assert sol.majorityElement([0,0,0,0,1,2,3]) == 0
assert sol.majorityElement([10**9, 10**9, -(10**9)]) == 10**9
assert sol.majorityElement([1,2,3,4,5,6,1,1,1,1,1]) == 1
assert sol.majorityElement([4,1,4,2,4,3,4]) == 4
assert sol.majorityElement([5,5,5,5,5,1,2,3,4]) == 5