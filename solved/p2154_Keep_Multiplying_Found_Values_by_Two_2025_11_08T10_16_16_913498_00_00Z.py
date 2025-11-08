"""
URL: https://leetcode.com/problems/keep-multiplying-found-values-by-two/description/?envType=problem-list-v2&envId=vn57k9wr

2154. Keep Multiplying Found Values by Two

You are given an array of integers nums. You are also given an integer original which is the first number that needs to be searched for in nums.

You then do the following steps:

1. If original is found in nums, multiply it by two (i.e., set original = 2 * original).

2. Otherwise, stop the process.

3. Repeat this process with the new number as long as you keep finding the number.

Return the final value of original.

Example 1:

Input: nums = [5,3,6,1,12], original = 3
Output: 24
Explanation:
- 3 is found in nums. 3 is multiplied by 2 to obtain 6.
- 6 is found in nums. 6 is multiplied by 2 to obtain 12.
- 12 is found in nums. 12 is multiplied by 2 to obtain 24.
- 24 is not found in nums. Thus, 24 is returned.

Example 2:

Input: nums = [2,7,9], original = 4
Output: 4
Explanation:
- 4 is not found in nums. Thus, 4 is returned.

Constraints:

    1 <= nums.length <= 1000
    1 <= nums[i], original <= 1000
"""


class Solution:
    def findFinalValue(self, nums: List[int], original: int) -> int:
        nums = set(nums)
        while original in nums:
            original *= 2
        return original


sol = Solution()

# print(sol.findFinalValue([5, 3, 6, 1, 12], 3))  # 24

assert sol.findFinalValue([5, 3, 6, 1, 12], 3) == 24
assert sol.findFinalValue([2, 7, 9], 4) == 4
assert sol.findFinalValue([1], 1) == 2
assert sol.findFinalValue([1, 2], 1) == 4
assert sol.findFinalValue([2, 4, 8, 16], 1) == 1
assert sol.findFinalValue([1, 2, 4, 8, 16, 32, 64, 128, 256, 512], 1) == 1024
assert sol.findFinalValue([1000], 1000) == 2000
assert sol.findFinalValue([1000], 500) == 500
assert sol.findFinalValue([4, 8, 2, 16], 2) == 32
assert sol.findFinalValue([5, 3, 6, 1, 12, 24], 3) == 48
assert sol.findFinalValue([3, 3, 6, 12], 3) == 24
assert sol.findFinalValue([1, 3, 5, 7, 9], 2) == 2
