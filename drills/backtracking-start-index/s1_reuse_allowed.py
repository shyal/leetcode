"""
DRILL: Reuse Allowed
TRAINS: backtracking-start-index

Given an array nums of distinct positive integers and an integer target,
return every combination of numbers from nums that sums to target. A
number may be taken any number of times. Each combination lists its
numbers in non-decreasing order, and two combinations holding the same
numbers the same number of times are the same combination.

Example 1:

Input: nums = [2, 3, 6, 7], target = 7
Output: [[2, 2, 3], [7]]
Explanation: [3, 2, 2] is not listed. It holds the same numbers as
[2, 2, 3].

Example 2:

Input: nums = [2], target = 1
Output: []
Explanation: no number of 2s sums to 1.

Example 3:

Input: nums = [3], target = 9
Output: [[3, 3, 3]]

Constraints:

    1 <= len(nums) <= 30
    1 <= nums[i] <= 40
    1 <= target <= 40
    The values in nums are distinct and given in increasing order.

    REQUIRED: [3, 2, 2] is never built, not built and discarded. Stop a
    branch the moment the running sum passes target. NO de-duplicating
    the answer at the end, NO counting how many times each number was
    taken.
"""


class Solution:
    def combinationSum(self, nums: list[int], target: int) -> list[list[int]]:
        pass


sol = Solution()

print(sol.combinationSum([2, 3, 6, 7], 7))  # [[2, 2, 3], [7]]

# assert sorted(map(tuple, sol.combinationSum([2, 3, 6, 7], 7))) == [(2, 2, 3), (7,)]
# assert sol.combinationSum([2], 1) == []
# assert sol.combinationSum([3], 9) == [[3, 3, 3]]
# assert sorted(map(tuple, sol.combinationSum([2, 3, 5], 8))) == [
#     (2, 2, 2, 2), (2, 3, 3), (3, 5)
# ]

# res = sol.combinationSum([1, 2], 5)
# assert len(res) == 3 and len({tuple(c) for c in res}) == 3
# assert all(sum(c) == 5 and c == sorted(c) for c in res)

# assert len(sol.combinationSum([2, 4, 6, 8], 8)) == 5
