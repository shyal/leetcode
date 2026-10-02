"""
DRILL: Permutations

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

    REQUIRED: every call loops over ALL of nums, from index 0. Deciding
    in O(1) whether an element is already in the ordering being built is
    the drill. NO start index, NO swapping elements of nums, NO removing
    them from the list, no scanning the ordering to test membership.
"""


# mu 0.7
# def permute(nums: [int]) -> [[int]]
#   def helper(i)
#     if len(path) == len(nums)
#       res <- path[::]
#     for j in range(len(nums))
#       if used[j]
#         continue
#       used[j] = True
#       path <- nums[j]
#       helper(j + 1)
#       path .
#       used[j] = False
#   ret res, path, used = [], [], table(len(nums), False)
#   helper(0)

def table(*dims, fill=0):
    if len(dims) == 1:
        return [fill] * dims[0]
    if len(dims) == 2:
        return [[fill] * dims[1] for _ in range(dims[0])]
    return [table(*dims[1:], fill=fill) for _ in range(dims[0])]


class Solution:
    def permute(self, nums: list[int]) -> list[list[int]]:
        def helper(i):
            if len(path) == len(nums):
                res.append(path[::])
            for j in range(len(nums)):
                if used[j]:
                    continue
                used[j] = True
                path.append(nums[j])
                helper(j + 1)
                path.pop()
                used[j] = False
        res, path, used = [], [], table(len(nums), False)
        helper(0)
        return res


sol = Solution()
print(sol.permute([1, 2, 3]))
assert sorted(map(tuple, sol.permute([1, 2, 3]))) == [(1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 1, 2), (3, 2, 1)]
assert sol.permute([5]) == [[5]]
assert sorted(map(tuple, sol.permute([9, 4]))) == [(4, 9), (9, 4)]
res = sol.permute([1, 2, 3, 4])
assert len(res) == 24 and len({tuple(p) for p in res}) == 24
assert all((sorted(p) == [1, 2, 3, 4] for p in res))
res = sol.permute(list(range(0, 8)))
assert len(res) == 40320 and len({tuple(p) for p in res}) == 40320
