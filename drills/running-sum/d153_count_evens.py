"""
DRILL: Count Evens

Given an integer array nums, return how many elements of nums are even.

Example 1:

Input: nums = [3, 4, 7, 8, 9]
Output: 2
Explanation: 4 and 8 are even.

Example 2:

Input: nums = [1, 3, 5]
Output: 0

Example 3:

Input: nums = [-2, 0, 2]
Output: 3
Explanation: 0 and -2 are even.

Constraints:

    1 <= len(nums) <= 10^5
    -1000 <= nums[i] <= 1000

    REQUIRED: O(n), one expression. NO accumulator variable. NO loop
    statement. NO list built to take its length.
"""


class Solution:

    def countEvens(self, nums: List[int]) -> int:
        pass


sol = Solution()

print(sol.countEvens([3, 4, 7, 8, 9]))  # 2

# assert sol.countEvens([3, 4, 7, 8, 9]) == 2
# assert sol.countEvens([1, 3, 5]) == 0
# assert sol.countEvens([-2, 0, 2]) == 3
# assert sol.countEvens([2, 1, 1]) == 1
# assert sol.countEvens([1, 1, 2]) == 1
# assert sol.countEvens([1, 2, 1]) == 1
# assert sol.countEvens([7]) == 0
# assert sol.countEvens([6]) == 1
# assert sol.countEvens(list(range(-1000, 1000))) == 1000
