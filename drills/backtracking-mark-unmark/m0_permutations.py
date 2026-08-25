"""
DRILL: Permutations
TRAINS: backtracking-mark-unmark

Given an array nums of distinct integers, return every ordering of all of
them. The orderings may come back in any order.

Example 1:

Input: nums = [1, 2, 3]
Output: [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
Explanation: [1, 2] is not listed. Every ordering uses all of nums.

Example 2:

Input: nums = [5]
Output: [[5]]

Constraints:

    1 <= len(nums) <= 8
    -10^9 <= nums[i] <= 10^9
    The values in nums are distinct.

    REQUIRED: every call loops over ALL of nums, from index 0. A separate
    list of flags, one per index, says which elements are already in the
    ordering being built; a flagged element is skipped. Raise the flag
    before the recursive call and lower it after, in the same place the
    path is appended and popped. NO start index - order matters here, so
    an element passed over at one depth must still be available at the
    next. NO swapping elements of nums, NO removing them from the list.
"""


class Solution:
    def permute(self, nums: list[int]) -> list[list[int]]:
        pass


sol = Solution()

print(sol.permute([1, 2, 3]))  # 6 orderings

# assert sorted(map(tuple, sol.permute([1, 2, 3]))) == [
#     (1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 1, 2), (3, 2, 1)
# ]
# assert sol.permute([5]) == [[5]]
# assert sorted(map(tuple, sol.permute([9, 4]))) == [(4, 9), (9, 4)]

# res = sol.permute([1, 2, 3, 4])
# assert len(res) == 24 and len({tuple(p) for p in res}) == 24
# assert all(sorted(p) == [1, 2, 3, 4] for p in res)

# res = sol.permute(list(range(8)))
# assert len(res) == 40320 and len({tuple(p) for p in res}) == 40320
