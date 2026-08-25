"""
DRILL: Take It or Leave It
TRAINS: backtracking-choose-undo

Given an array nums of distinct integers, return every subset of nums.
A subset lists its elements in the order they appear in nums. The subsets
may come back in any order, and the empty subset counts.

Example 1:

Input: nums = [1, 2, 3]
Output: [[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]

Example 2:

Input: nums = [5]
Output: [[], [5]]
Explanation: one element is either in or out, so there are two subsets.

Constraints:

    1 <= len(nums) <= 16
    -10^9 <= nums[i] <= 10^9
    The values in nums are distinct.

    REQUIRED: exactly one list holds the subset under construction, for
    the whole run. Grow it with append, recurse, then pop the element
    back off before the next branch. NO building a fresh list per branch
    (no `path + [x]`, no slicing, no copying on the way down), NO
    itertools. The one copy allowed is the one you record when a subset
    is complete: record the list itself and every answer ends up empty,
    because the run keeps mutating it.

---

Still had to peek. Forgot that this is a pick / ignore algo and thus
doesn't use a loop.

"""


class Solution:
    def subsets(self, nums: list[int]) -> list[list[int]]:
        def walk(i):
            if i == len(nums):
                res.append(path[:])
                return
            path.append(nums[i])
            walk(i + 1)
            path.pop()
            walk(i + 1)

        res = []
        path = []
        walk(0)
        return res


sol = Solution()

print(sol.subsets([1, 2, 3]))  # 8 subsets

assert sorted(map(tuple, sol.subsets([1, 2, 3]))) == [
    (),
    (1,),
    (1, 2),
    (1, 2, 3),
    (1, 3),
    (2,),
    (2, 3),
    (3,),
]
assert sorted(map(tuple, sol.subsets([5]))) == [(), (5,)]
assert sorted(map(tuple, sol.subsets([9, 4]))) == [(), (4,), (9,), (9, 4)]

res = sol.subsets([1, 2, 3, 4, 5])
assert len(res) == 32
assert len({tuple(s) for s in res}) == 32

res = sol.subsets(list(range(16)))
assert len(res) == 65536
assert all(s == sorted(s) for s in res)
