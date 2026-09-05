"""
DRILL: No Repeat Siblings
TRAINS: backtracking-dedupe-siblings
SNIPPET: lcsubsets

Given an array nums sorted in non-decreasing order that may hold repeated
values, return every distinct subset of nums. Two subsets holding the same
values the same number of times are the same subset. Each subset lists its
values in the order they appear in nums, and the subsets may come back in
any order. The move this drill trains works only on sorted input; nums
arrives sorted so that move is the whole task.

Example 1:

Input: nums = [1, 2, 2]
Output: [[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]
Explanation: nums holds two 2s, so [2, 2] is a subset, but [2] appears
once even though either 2 could fill it.

Example 2:

Input: nums = [4, 4, 4]
Output: [[], [4], [4, 4], [4, 4, 4]]

Constraints:

    1 <= len(nums) <= 12
    -10 <= nums[i] <= 10
    nums[i] <= nums[i + 1]

    REQUIRED: one backtracking pass. A subset joins the answer the
    moment it is built, and no subset is ever built twice. NO set or
    tuple de-duplication of the answer, NO Counter of the input, no
    comparing a candidate against subsets already collected. NO sort
    of nums.
"""


class Solution:
    def subsetsWithDup(self, nums: list[int]) -> list[list[int]]:
        pass


sol = Solution()

print(sol.subsetsWithDup([1, 2, 2]))  # 6 subsets

# assert sorted(map(tuple, sol.subsetsWithDup([1, 2, 2]))) == [
#     (), (1,), (1, 2), (1, 2, 2), (2,), (2, 2)
# ]
# assert sorted(map(tuple, sol.subsetsWithDup([4, 4, 4]))) == [
#     (), (4,), (4, 4), (4, 4, 4)
# ]
# assert sorted(map(tuple, sol.subsetsWithDup([1, 2]))) == [(), (1,), (1, 2), (2,)]
# assert sorted(map(tuple, sol.subsetsWithDup([-3, -3, 0, 7]))) == [
#     (), (-3,), (-3, -3), (-3, -3, 0), (-3, -3, 0, 7), (-3, -3, 7),
#     (-3, 0), (-3, 0, 7), (-3, 7), (0,), (0, 7), (7,)
# ]

# res = sol.subsetsWithDup([1, 1, 2, 2])
# assert len(res) == 9 and len({tuple(s) for s in res}) == 9

# res = sol.subsetsWithDup([5] * 12)
# assert len(res) == 13
