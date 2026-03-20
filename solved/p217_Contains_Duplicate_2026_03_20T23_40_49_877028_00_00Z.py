"""
URL: https://leetcode.com/problems/contains-duplicate/description/?envType=problem-list-v2&envId=vn57k9wr

217. Contains Duplicate

Given an integer array nums, return true if any value appears at least twice in the array, and return false if every element is distinct.


Example 1:

Input: nums = [1,2,3,1]
Output: true
Explanation: The element 1 occurs at the indices 0 and 3.

Example 2:

Input: nums = [1,2,3,4]
Output: false
Explanation: All elements are distinct.

Example 3:

Input: nums = [1,1,1,3,3,4,3,2,4,2]
Output: true


Constraints:

    1 <= nums.length <= 10^5
    -10^9 <= nums[i] <= 10^9
"""


class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        return len(set(nums)) < len(nums)


sol = Solution()

print(sol.containsDuplicate([1,2,3,1]))  # True

assert sol.containsDuplicate([1,2,3,1]) == True
assert sol.containsDuplicate([1,2,3,4]) == False
assert sol.containsDuplicate([1,1,1,3,3,4,3,2,4,2]) == True
assert sol.containsDuplicate([1]) == False
assert sol.containsDuplicate([1,1]) == True
assert sol.containsDuplicate([1,2]) == False
assert sol.containsDuplicate([0,0,0]) == True
assert sol.containsDuplicate([-1,-1]) == True
assert sol.containsDuplicate([-1,0,1]) == False
assert sol.containsDuplicate([0,-1,0]) == True
assert sol.containsDuplicate([1,2,3,4,1]) == True
assert sol.containsDuplicate([1000000000, -1000000000, 0]) == False
assert sol.containsDuplicate([1000000000, -1000000000, 1000000000]) == True