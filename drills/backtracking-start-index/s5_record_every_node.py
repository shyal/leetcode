"""
DRILL: Record Every Node
TRAINS: backtracking-start-index
SNIPPET: lccomb

Given an array nums of distinct integers, return every subset of nums,
including the empty subset. List each subset in the order its elements
appear in nums. The subsets themselves can be returned in any order.

Example 1:

Input: nums = [1, 2, 3]
Output: [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]

Example 2:

Input: nums = [7]
Output: [[], [7]]

Constraints:

    1 <= len(nums) <= 16
    -10^9 <= nums[i] <= 10^9
    The elements of nums are distinct.

    REQUIRED: one recursive pass that records every subset exactly once,
    when it is built. NO include-or-exclude branch per element, NO
    bitmask, NO itertools.
"""


class Solution:
    def subsets(self, nums: list[int]) -> list[list[int]]:
        pass


sol = Solution()

print(sol.subsets([1, 2, 3]))  # [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]

# assert sorted(map(tuple, sol.subsets([1, 2, 3]))) == [
#     (), (1,), (1, 2), (1, 2, 3), (1, 3), (2,), (2, 3), (3,)
# ]
# assert sorted(map(tuple, sol.subsets([7]))) == [(), (7,)]
# assert sorted(map(tuple, sol.subsets([9, 4]))) == [(), (4,), (9,), (9, 4)]

# res = sol.subsets([1, 2, 3, 4, 5])
# assert len(res) == 32 and len({tuple(s) for s in res}) == 32

# res = sol.subsets(list(range(16)))
# assert len(res) == 65536
# assert all(s == sorted(s) for s in res)
