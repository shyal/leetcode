"""
URL: https://leetcode.com/problems/permutations-ii/description/?envType=problem-list-v2&envId=vn57k9wr

47. Permutations II

Given a collection of numbers, nums, that might contain duplicates, return all possible unique permutations in any order.

Example 1:

Input: nums = [1,1,2]
Output:
[
 [1,1,2],
 [1,2,1],
 [2,1,1]
]

Example 2:

Input: nums = [1,2,3]
Output:
[
 [1,2,3],
 [1,3,2],
 [2,1,3],
 [2,3,1],
 [3,1,2],
 [3,2,1]
]

Constraints:

    1 <= nums.length <= 8
    -10 <= nums[i] <= 10
---
hinted

LEETCODE: Accepted (3 ms, 19.8 MB)
"""


# mu 0.7
# def permuteUnique(nums: [int]) -> [[int]]
#   def helper()
#     if len path == len nums
#       res <- path[:]
#       return
#     seen = set([])
#     for j in range(len(nums))
#       if use[j] or nums[j] in seen
#         continue
#       seen.add(nums[j])
#       path <- nums[j]
#       use[j] = True
#       helper()
#       use[j] = False
#       path .
#
#   res, path, use = [], [], table(len(nums), fill=False)
#   helper()
#   [*sorted(res)]

def table(*dims, fill=0):
    if len(dims) == 1:
        return [fill] * dims[0]
    if len(dims) == 2:
        return [[fill] * dims[1] for _ in range(dims[0])]
    return [table(*dims[1:], fill=fill) for _ in range(dims[0])]


class Solution:
    def permuteUnique(self, nums: list[int]) -> list[list[int]]:
        def helper():
            if len(path) == len(nums):
                res.append(path[:])
                return
            seen = set([])
            for j in range(len(nums)):
                if use[j] or nums[j] in seen:
                    continue
                seen.add(nums[j])
                path.append(nums[j])
                use[j] = True
                helper()
                use[j] = False
                path.pop()
        res, path, use = [], [], table(len(nums), fill=False)
        helper()
        return [*sorted(res)]


sol = Solution()
print(sol.permuteUnique([1, 1, 2]))
assert sol.permuteUnique([1, 1, 2]) == [[1, 1, 2], [1, 2, 1], [2, 1, 1]]
assert sol.permuteUnique([1, 2, 3]) == [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
assert sol.permuteUnique([]) == [[]]
assert sol.permuteUnique([1]) == [[1]]
assert sol.permuteUnique([2, 2, 2]) == [[2, 2, 2]]
assert sol.permuteUnique([-1, -1, 0]) == [[-1, -1, 0], [-1, 0, -1], [0, -1, -1]]
assert sol.permuteUnique([0, 0, 0, 0]) == [[0, 0, 0, 0]]
assert sol.permuteUnique([1, 2, 2, 3]) == [[1, 2, 2, 3], [1, 2, 3, 2], [1, 3, 2, 2], [2, 1, 2, 3], [2, 1, 3, 2], [2, 2, 1, 3], [2, 2, 3, 1], [2, 3, 1, 2], [2, 3, 2, 1], [3, 1, 2, 2], [3, 2, 1, 2], [3, 2, 2, 1]]
assert sol.permuteUnique([10, -10, 10]) == [[-10, 10, 10], [10, -10, 10], [10, 10, -10]]
assert sol.permuteUnique([1, 1, 1, 2, 2]) == [[1, 1, 1, 2, 2], [1, 1, 2, 1, 2], [1, 1, 2, 2, 1], [1, 2, 1, 1, 2], [1, 2, 1, 2, 1], [1, 2, 2, 1, 1], [2, 1, 1, 1, 2], [2, 1, 1, 2, 1], [2, 1, 2, 1, 1], [2, 2, 1, 1, 1]]
assert sol.permuteUnique([-10, -10, -10, -10]) == [[-10, -10, -10, -10]]
assert sol.permuteUnique([0]) == [[0]]
