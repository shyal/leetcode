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

    REQUIRED: every call loops over ALL of nums, from index 0. Deciding
    in O(1) whether an element is already in the ordering being built is
    the drill. NO start index, NO swapping elements of nums, NO removing
    them from the list, no scanning the ordering to test membership.

---

Learning.

"""


class Solution:
    def permute(self, nums: list[int]) -> list[list[int]]:
        res, path = [], []
        used = [False] * len(nums)

        def rec():
            if len(path) == len(nums):
                res.append(path[:])
            for i in range(len(nums)):
                if used[i]:
                    continue
                used[i] = True
                path.append(nums[i])
                rec()
                path.pop()
                used[i] = False

        rec()

        return res


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
