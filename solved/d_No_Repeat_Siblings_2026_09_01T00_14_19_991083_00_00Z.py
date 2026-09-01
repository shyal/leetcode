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

    REQUIRED: one backtracking pass. A subset joins the answer the
    moment it is built, and no subset is ever built twice. NO set or
    tuple de-duplication of the answer, NO Counter of the input, no
    comparing a candidate against subsets already collected.


---

Learning.

"""


class Solution:
    def subsetsWithDup(self, nums: list[int]) -> list[list[int]]:
        def helper(i):
            ret.append(curr[:])
            for j in range(i, len(nums)):
                if j > i and nums[j] == nums[j - 1]:
                    continue
                curr.append(nums[j])
                helper(j + 1)
                curr.pop()

        ret = []
        curr = []
        nums.sort()
        helper(0)
        return ret


sol = Solution()

print(sol.subsetsWithDup([1, 2, 2]))  # 6 subsets

assert sorted(map(tuple, sol.subsetsWithDup([1, 2, 2]))) == [
    (),
    (1,),
    (1, 2),
    (1, 2, 2),
    (2,),
    (2, 2),
]
assert sorted(map(tuple, sol.subsetsWithDup([4, 4, 4]))) == [
    (),
    (4,),
    (4, 4),
    (4, 4, 4),
]
assert sorted(map(tuple, sol.subsetsWithDup([1, 2]))) == [(), (1,), (1, 2), (2,)]
assert sorted(map(tuple, sol.subsetsWithDup([2, 1, 2]))) == [
    (),
    (1,),
    (1, 2),
    (1, 2, 2),
    (2,),
    (2, 2),
]

res = sol.subsetsWithDup([1, 1, 2, 2])
assert len(res) == 9 and len({tuple(s) for s in res}) == 9

res = sol.subsetsWithDup([5] * 12)
assert len(res) == 13
