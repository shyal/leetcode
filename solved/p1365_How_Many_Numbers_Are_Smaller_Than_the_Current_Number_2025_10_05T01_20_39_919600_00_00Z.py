"""
URL: https://leetcode.com/problems/how-many-numbers-are-smaller-than-the-current-number/description/

1365. How Many Numbers Are Smaller Than the Current Number

Given the array nums, for each nums[i] find out how many numbers in the array are smaller than it. That is, for each nums[i] you have to count the number of valid j's such that j != i and nums[j] < nums[i].

Return the answer in an array.


Example 1:

Input: nums = [8,1,2,2,3]

Output: [4,0,1,1,3]

Example 2:

Input: nums = [6,5,4,8]

Output: [2,1,0,3]

Example 3:

Input: nums = [7,7,7,7]

Output: [0,0,0,0]


Constraints:

        2 <= nums.length <= 500
        0 <= nums[i] <= 100

"""


class Solution:
    def smallerNumbersThanCurrent(self, nums: List[int]) -> List[int]:
        res = []
        for i in range(len(nums)):
            count = 0
            for j in range(len(nums)):
                if i != j:
                    if nums[j] < nums[i]:
                        count += 1
            res.append(count)
        return res


sol = Solution()

nums = [8, 1, 2, 2, 3]

assert sol.smallerNumbersThanCurrent(nums) == [4, 0, 1, 1, 3]

nums = [6, 5, 4, 8]
assert sol.smallerNumbersThanCurrent(nums) == [2, 1, 0, 3]

nums = [7, 7, 7, 7]
assert sol.smallerNumbersThanCurrent(nums) == [0, 0, 0, 0]

nums = [0, 1]
assert sol.smallerNumbersThanCurrent(nums) == [0, 1]

nums = [1, 0]
assert sol.smallerNumbersThanCurrent(nums) == [1, 0]

nums = [0, 0]
assert sol.smallerNumbersThanCurrent(nums) == [0, 0]

nums = [100, 100, 100]
assert sol.smallerNumbersThanCurrent(nums) == [0, 0, 0]

nums = [1, 2, 3, 4, 5]
assert sol.smallerNumbersThanCurrent(nums) == [0, 1, 2, 3, 4]

nums = [5, 4, 3, 2, 1]
assert sol.smallerNumbersThanCurrent(nums) == [4, 3, 2, 1, 0]
