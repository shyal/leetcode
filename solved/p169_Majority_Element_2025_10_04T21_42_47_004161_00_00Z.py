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

    n == nums.length
    1 <= n <= 5 * 104
    -109 <= nums[i] <= 109


Follow-up: Could you solve the problem in linear time and in O(1) space?
"""


class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        guess = nums[0]
        count = 1
        for i in range(1, len(nums)):
            if count == 0:
                guess = nums[i]
                count = 1
            else:
                if nums[i] == guess:
                    count += 1
                else:
                    count -= 1
        return guess


sol = Solution()

assert sol.majorityElement([3, 2, 3]) == 3
assert sol.majorityElement([2, 2, 1, 1, 1, 2, 2]) == 2
assert sol.majorityElement([3, 2, 3]) == 3
assert sol.majorityElement([2, 2, 1, 1, 1, 2, 2]) == 2
assert sol.majorityElement([1]) == 1
assert sol.majorityElement([1, 1]) == 1
assert sol.majorityElement([1, 2, 1]) == 1
assert sol.majorityElement([2, 1, 1]) == 1
assert sol.majorityElement([1, 1, 2]) == 1
assert sol.majorityElement([6, 5, 5]) == 5
assert sol.majorityElement([1, 2, 1, 1, 3]) == 1
assert sol.majorityElement([-1, -2, -1]) == -1
assert sol.majorityElement([1000000000, 1000000000, 999999999]) == 1000000000
assert sol.majorityElement([1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2]) == 1
assert sol.majorityElement([1, 2, 3, 1, 1, 1]) == 1
assert sol.majorityElement([4, 5, 4, 6, 4, 4, 8]) == 4
assert sol.majorityElement([-1000000000]) == -1000000000
