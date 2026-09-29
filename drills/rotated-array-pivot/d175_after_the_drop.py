"""
DRILL: After The Drop
TRAINS: rotated-array-pivot

Given a rotated sorted array nums of distinct integers, return a list
of booleans. There is at most one index d with nums[d] < nums[d - 1].
Entry i is True when i >= d. If no such d exists, every entry is True.

Example 1:

Input: nums = [6, 8, 9, 1, 3]
Output: [False, False, False, True, True]
Explanation: d = 3, because 1 < 9.

Example 2:

Input: nums = [2, 4, 5, 7]
Output: [True, True, True, True]

Example 3:

Input: nums = [9, 1, 3, 5, 7]
Output: [False, True, True, True, True]

Constraints:

    1 <= len(nums) <= 5000
    -5000 <= nums[i] <= 5000
    All values of nums are distinct.

    REQUIRED: O(n), one comparison per element, against ONE fixed
    element. NO scan for d, NO sorting, NO min().
"""


class Solution:
    def afterTheDrop(self, nums: List[int]) -> List[bool]:
        pass


sol = Solution()

print(sol.afterTheDrop([6, 8, 9, 1, 3]))  # [False, False, False, True, True]

# assert sol.afterTheDrop([6, 8, 9, 1, 3]) == [False, False, False, True, True]
# assert sol.afterTheDrop([2, 4, 5, 7]) == [True, True, True, True]
# assert sol.afterTheDrop([9, 1, 3, 5, 7]) == [False, True, True, True, True]
# assert sol.afterTheDrop([3, 5, 7, 9, 1]) == [False, False, False, False, True]
# assert sol.afterTheDrop([5]) == [True]
# assert sol.afterTheDrop([4, 5, 6, 7, 0, 1, 2]) == [False, False, False, False, True, True, True]
# assert sol.afterTheDrop([-2, -1, -5, -4, -3]) == [False, False, True, True, True]
