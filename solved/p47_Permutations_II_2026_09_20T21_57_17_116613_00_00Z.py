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

This feels like magic, and i don't feel like spending 30 minutes
parsing a recursion tree

if j > 0 and nums[j] == nums[j - 1] and not used[j - 1]:

So i'll mark it as assisted.

I could have solved it easily with a seen set though.

LEETCODE: Accepted (3 ms, 19.9 MB)
"""


class Solution:
    def permuteUnique(self, nums: List[int]) -> List[List[int]]:
        def helper(i):
            if len(path) == len(nums):
                res.append(path[:])
                return

            for j in range(len(nums)):
                if used[j]:
                    continue
                if j > 0 and nums[j] == nums[j - 1] and not used[j - 1]:
                    continue

                path.append(nums[j])
                used[j] = True
                helper(j + 1)
                used[j] = False
                path.pop()

        nums.sort()
        res, path, used = [], [], [False] * len(nums)
        helper(0)
        return res


sol = Solution()

print(sol.permuteUnique([1, 1, 2]))  # [[1,1,2],[1,2,1],[2,1,1]]

assert sol.permuteUnique([1, 1, 2]) == [[1, 1, 2], [1, 2, 1], [2, 1, 1]]
assert sol.permuteUnique([1, 2, 3]) == [
    [1, 2, 3],
    [1, 3, 2],
    [2, 1, 3],
    [2, 3, 1],
    [3, 1, 2],
    [3, 2, 1],
]

assert sol.permuteUnique([]) == [[]]
assert sol.permuteUnique([1]) == [[1]]
assert sol.permuteUnique([2, 2, 2]) == [[2, 2, 2]]
assert sol.permuteUnique([-1, -1, 0]) == [[-1, -1, 0], [-1, 0, -1], [0, -1, -1]]
assert sol.permuteUnique([0, 0, 0, 0]) == [[0, 0, 0, 0]]
assert sol.permuteUnique([1, 2, 2, 3]) == [
    [1, 2, 2, 3],
    [1, 2, 3, 2],
    [1, 3, 2, 2],
    [2, 1, 2, 3],
    [2, 1, 3, 2],
    [2, 2, 1, 3],
    [2, 2, 3, 1],
    [2, 3, 1, 2],
    [2, 3, 2, 1],
    [3, 1, 2, 2],
    [3, 2, 1, 2],
    [3, 2, 2, 1],
]
assert sol.permuteUnique([10, -10, 10]) == [[-10, 10, 10], [10, -10, 10], [10, 10, -10]]
assert sol.permuteUnique([1, 1, 1, 2, 2]) == [
    [1, 1, 1, 2, 2],
    [1, 1, 2, 1, 2],
    [1, 1, 2, 2, 1],
    [1, 2, 1, 1, 2],
    [1, 2, 1, 2, 1],
    [1, 2, 2, 1, 1],
    [2, 1, 1, 1, 2],
    [2, 1, 1, 2, 1],
    [2, 1, 2, 1, 1],
    [2, 2, 1, 1, 1],
]
assert sol.permuteUnique([-10, -10, -10, -10]) == [[-10, -10, -10, -10]]
assert sol.permuteUnique([0]) == [[0]]
