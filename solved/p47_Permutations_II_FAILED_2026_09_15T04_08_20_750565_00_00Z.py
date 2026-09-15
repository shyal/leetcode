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

LEETCODE: Wrong Answer (26/33 cases)
"""


class Solution:
    def permuteUnique(self, nums: List[int]) -> List[List[int]]:
        def helper(i):
            if len(path) == len(nums):
                res.append(tuple(path[:]))
                return

            for j in range(len(nums)):
                if j > i and nums[j] == nums[j - 1]:
                    continue
                if not use[j]:
                    continue
                use[j] = False
                path.append(nums[j])
                helper(j + 1)
                use[j] = True
                path.pop()

        path, use, res = [], [True] * len(nums), []
        helper(0)
        return [list(x) for x in set(res)]


sol = Solution()

print(sol.permuteUnique([1, 1, 2]))  # [[1,1,2],[1,2,1],[2,1,1]]

# assert sol.permuteUnique([1, 1, 2]) == [[1, 1, 2], [1, 2, 1], [2, 1, 1]]
# assert sol.permuteUnique([1, 2, 3]) == [
#     [1, 2, 3],
#     [1, 3, 2],
#     [2, 1, 3],
#     [2, 3, 1],
#     [3, 1, 2],
#     [3, 2, 1],
# ]

# assert sol.permuteUnique([]) == [[]]
# assert sol.permuteUnique([1]) == [[1]]
# assert sol.permuteUnique([2, 2, 2]) == [[2, 2, 2]]
# assert sol.permuteUnique([-1, -1, 0]) == [[-1, -1, 0], [-1, 0, -1], [0, -1, -1]]
# assert sol.permuteUnique([0, 0, 0, 0]) == [[0, 0, 0, 0]]
# assert sol.permuteUnique([1, 2, 2, 3]) == [
#     [1, 2, 2, 3],
#     [1, 2, 3, 2],
#     [1, 3, 2, 2],
#     [2, 1, 2, 3],
#     [2, 1, 3, 2],
#     [2, 2, 1, 3],
#     [2, 2, 3, 1],
#     [2, 3, 1, 2],
#     [2, 3, 2, 1],
#     [3, 1, 2, 2],
#     [3, 2, 1, 2],
#     [3, 2, 2, 1],
# ]
# assert sol.permuteUnique([10, -10, 10]) == [[-10, 10, 10], [10, -10, 10], [10, 10, -10]]
# assert sol.permuteUnique([1, 1, 1, 2, 2]) == [
#     [1, 1, 1, 2, 2],
#     [1, 1, 2, 1, 2],
#     [1, 1, 2, 2, 1],
#     [1, 2, 1, 1, 2],
#     [1, 2, 1, 2, 1],
#     [1, 2, 2, 1, 1],
#     [2, 1, 1, 1, 2],
#     [2, 1, 1, 2, 1],
#     [2, 1, 2, 1, 1],
#     [2, 2, 1, 1, 1],
# ]
# assert sol.permuteUnique([-10, -10, -10, -10]) == [[-10, -10, -10, -10]]
# assert sol.permuteUnique([0]) == [[0]]


# FAILED: walked away after 7m 10s; no working solution.
# Judge the moves actually attempted as struggled, not clean.
