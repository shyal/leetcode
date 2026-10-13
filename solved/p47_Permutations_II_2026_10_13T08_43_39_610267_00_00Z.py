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

LEETCODE: Accepted (3 ms, 20 MB)
"""


# mu 0.10
# class Solution
#   def permuteUnique(nums: [int]) -> [[int]]
#     def helper()
#       if len path == len nums
#         res <- path[:]
#       seen = set()
#       for >j in nums
#         if used[j] or nums[j] in seen
#           continue
#         seen.add(nums[j])
#         used[j] = True
#         path <- nums[j]
#         helper()
#         path .
#         used[j] = False
#     ret res, path, used = [], [], table(len(nums), fill=False)
#     nums.sort()
#     helper()

def table(*dims, fill=0):
    if len(dims) == 1:
        return [fill] * dims[0]
    return [table(*dims[1:], fill=fill) for _ in range(dims[0])]


class Solution:
    def permuteUnique(self, nums: list[int]) -> list[list[int]]:
        def helper():
            if len(path) == len(nums):
                res.append(path[:])
            seen = set()
            for j in range(len(nums)):
                if used[j] or nums[j] in seen:
                    continue
                seen.add(nums[j])
                used[j] = True
                path.append(nums[j])
                helper()
                path.pop()
                used[j] = False
        res, path, used = [], [], table(len(nums), fill=False)
        nums.sort()
        helper()
        return res


sol = Solution()
print(sol.permuteUnique([1, 1, 2]))
_l, _r = sol.permuteUnique([1, 1, 2]), [[1, 1, 2], [1, 2, 1], [2, 1, 1]]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.permuteUnique([1, 2, 3]), [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.permuteUnique([]), [[]]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.permuteUnique([1]), [[1]]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.permuteUnique([2, 2, 2]), [[2, 2, 2]]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.permuteUnique([-1, -1, 0]), [[-1, -1, 0], [-1, 0, -1], [0, -1, -1]]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.permuteUnique([0, 0, 0, 0]), [[0, 0, 0, 0]]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.permuteUnique([1, 2, 2, 3]), [[1, 2, 2, 3], [1, 2, 3, 2], [1, 3, 2, 2], [2, 1, 2, 3], [2, 1, 3, 2], [2, 2, 1, 3], [2, 2, 3, 1], [2, 3, 1, 2], [2, 3, 2, 1], [3, 1, 2, 2], [3, 2, 1, 2], [3, 2, 2, 1]]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.permuteUnique([10, -10, 10]), [[-10, 10, 10], [10, -10, 10], [10, 10, -10]]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.permuteUnique([1, 1, 1, 2, 2]), [[1, 1, 1, 2, 2], [1, 1, 2, 1, 2], [1, 1, 2, 2, 1], [1, 2, 1, 1, 2], [1, 2, 1, 2, 1], [1, 2, 2, 1, 1], [2, 1, 1, 1, 2], [2, 1, 1, 2, 1], [2, 1, 2, 1, 1], [2, 2, 1, 1, 1]]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.permuteUnique([-10, -10, -10, -10]), [[-10, -10, -10, -10]]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.permuteUnique([0]), [[0]]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
