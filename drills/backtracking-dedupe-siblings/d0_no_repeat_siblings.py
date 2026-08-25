"""
DRILL: No Repeat Siblings
TRAINS: backtracking-dedupe-siblings

Given an array nums that may hold repeated values, return every distinct
subset of nums. Each subset lists its values in non-decreasing order, and
two subsets holding the same values the same number of times are the same
subset. The subsets may come back in any order.

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

    REQUIRED: sort nums first, so equal values sit next to each other.
    Inside the loop, skip a value when it equals the one before it AND
    its index is past the start value for this call. The second half of
    that test is the drill: comparing the index against 0 instead of the
    start value throws away [2, 2], because the second 2 is then never
    allowed to follow the first. NO set or tuple de-duplication of the
    answer, NO Counter of the input.
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
# assert sorted(map(tuple, sol.subsetsWithDup([2, 1, 2]))) == [
#     (), (1,), (1, 2), (1, 2, 2), (2,), (2, 2)
# ]

# res = sol.subsetsWithDup([1, 1, 2, 2])
# assert len(res) == 9 and len({tuple(s) for s in res}) == 9

# res = sol.subsetsWithDup([5] * 12)
# assert len(res) == 13
