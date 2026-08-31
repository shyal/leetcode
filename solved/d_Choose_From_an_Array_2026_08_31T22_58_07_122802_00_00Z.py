"""
DRILL: Choose From an Array
TRAINS: backtracking-start-index

Given an array nums of distinct integers and an integer k, return every
combination of k elements of nums. List the elements of each combination
in the order they appear in nums. The combinations themselves can be
returned in any order.

Example 1:

Input: nums = [5, 1, 8], k = 2
Output: [[5, 1], [5, 8], [1, 8]]
Explanation: [1, 5] is the same combination as [5, 1], and 5 comes first
in nums.

Example 2:

Input: nums = [3, 7, 2], k = 3
Output: [[3, 7, 2]]

Constraints:

    1 <= len(nums) <= 20
    -10^9 <= nums[i] <= 10^9
    1 <= k <= len(nums)
    The elements of nums are distinct.

    REQUIRED: never build [1, 5], not even to discard it. NO sorting
    nums, NO used or visited set, NO itertools, NO de-duplicating the
    answer at the end.
"""


class Solution:
    def choose(self, nums: list[int], k: int) -> list[list[int]]:
        def helper(i):
            if len(curr) == k:
                ret.append(curr[:])
                return
            for j in range(i, len(nums)):
                curr.append(nums[j])
                helper(j + 1)
                curr.pop()

        ret = []
        curr = []
        helper(0)
        return ret


sol = Solution()

print(sol.choose([5, 1, 8], 2))  # [[5, 1], [5, 8], [1, 8]]

assert sorted(map(tuple, sol.choose([5, 1, 8], 2))) == [(1, 8), (5, 1), (5, 8)]
assert sol.choose([3, 7, 2], 3) == [[3, 7, 2]]
assert sol.choose([4], 1) == [[4]]
assert sorted(map(tuple, sol.choose([9, 4, 7, 1], 2))) == [
    (4, 1),
    (4, 7),
    (7, 1),
    (9, 1),
    (9, 4),
    (9, 7),
]

res = sol.choose(list(range(20)), 3)
assert len(res) == 1140 and len({tuple(c) for c in res}) == 1140
assert all(a < b < c for a, b, c in res)
