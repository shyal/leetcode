"""
URL: https://leetcode.com/problems/find-the-duplicate-number/description/

287. Find the Duplicate Number

Given an array of integers nums containing n + 1 integers where each integer is in the range [1, n] inclusive.

There is exactly one duplicate number in nums, return this duplicate number.

You must solve the problem without modifying the array nums and uses only constant extra space.


Example 1:

Input: nums = [1,3,4,2,2]
Output: 2

Example 2:

Input: nums = [3,1,3,4,2]
Output: 3


Constraints:

    1 <= n <= 105
    nums.length == n + 1
    1 <= nums[i] <= n
    All the integers in nums appear only once except for precisely one integer which appears two or more times.

---

Keeping this in learning mode.

"""


class Solution(object):

    def findDuplicate(self, nums):
        slow = nums[0]
        fast = nums[0]

        while True:
            slow = nums[slow]
            fast = nums[fast]
            if slow == fast:
                break

        # while slow == fast:


sol = Solution()
# sol.findDuplicate([3, 1, 3, 4, 2])

# assert sol.findDuplicate([1, 3, 4, 2, 2]) == 2
# assert sol.findDuplicate([3, 1, 3, 4, 2]) == 3
# assert sol.findDuplicate([1, 1]) == 1
# assert sol.findDuplicate([1, 2, 2, 3]) == 2
# assert sol.findDuplicate([3, 3, 3, 3]) == 3
# assert sol.findDuplicate([1, 2, 3, 4, 4]) == 4
# assert sol.findDuplicate([4, 1, 2, 3, 4]) == 4
# assert sol.findDuplicate([1, 2, 3, 1]) == 1
# assert sol.findDuplicate([2, 2, 2, 2, 2]) == 2

# assert sol.findDuplicate([1, 1, 1]) == 1
# assert sol.findDuplicate([2, 1, 2]) == 2
# assert sol.findDuplicate([4, 3, 1, 4, 2]) == 4
