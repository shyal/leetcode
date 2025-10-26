from typing import List

"""
URL: https://leetcode.com/problems/permutations-ii/description/?envType=problem-list-v2&envId=vn57k9wr

47. Permutations II

Given a collection of numbers, nums, that might contain duplicates, return all possible unique permutations in any order.

Example 1:

Input: nums = [1,1,2]
Output:
[[1,1,2],
 [1,2,1],
 [2,1,1]]

Example 2:

Input: nums = [1,2,3]
Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]

Constraints:

    1 <= nums.length <= 8
    -10 <= nums[i] <= 10

---


                                                        dfs(0)
                                                        |
                                    swap 0, 0        swap 0, 1      swap 0, 2
                                    [1, 1, 2]        [1, 1, 2]      [2, 1, 1] 

                            dfs(1)                    dfs(1)                    dfs(1)

swap 1, 1     swap 1, 2        
[1, 1, 2]     [1, 2, 1]


swap 2, 2     swap 2, 2
[1, 1, 2]     [1, 2, 1]

[1, 1, 2].    [1, 2, 1]

Hmm this feels like it's not the right solution, since i had to resort to using a set.

"""


class Solution:
    def permuteUnique(self, nums: List[int]) -> List[List[int]]:
        def dfs(i):
            if i == len(nums):
                res.add(tuple(nums[:]))
                return
            for j in range(i, len(nums)):
                if i != j and nums[i] == nums[j]:
                    continue
                nums[i], nums[j] = nums[j], nums[i]
                dfs(i + 1)
                nums[i], nums[j] = nums[j], nums[i]

        res = set()
        dfs(0)
        return list(map(list, res))


sol = Solution()

assert set(map(tuple, sol.permuteUnique([1, 1, 2]))) == set(
    map(tuple, [[1, 1, 2], [1, 2, 1], [2, 1, 1]])
)
assert set(map(tuple, sol.permuteUnique([1, 2, 3]))) == set(
    map(tuple, [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]])
)
assert set(map(tuple, sol.permuteUnique([1]))) == set(map(tuple, [[1]]))
assert set(map(tuple, sol.permuteUnique([1, 1]))) == set(map(tuple, [[1, 1]]))
assert set(map(tuple, sol.permuteUnique([1, 1, 1]))) == set(map(tuple, [[1, 1, 1]]))
assert set(map(tuple, sol.permuteUnique([-1, 1]))) == set(
    map(tuple, [[-1, 1], [1, -1]])
)
assert set(map(tuple, sol.permuteUnique([0, 0, 1]))) == set(
    map(tuple, [[0, 0, 1], [0, 1, 0], [1, 0, 0]])
)
assert set(map(tuple, sol.permuteUnique([1, 1, 2, 2]))) == set(
    map(
        tuple,
        [
            [1, 1, 2, 2],
            [1, 2, 1, 2],
            [1, 2, 2, 1],
            [2, 1, 1, 2],
            [2, 1, 2, 1],
            [2, 2, 1, 1],
        ],
    )
)
assert set(map(tuple, sol.permuteUnique([-1, 0, 1]))) == set(
    map(tuple, [[-1, 0, 1], [-1, 1, 0], [0, -1, 1], [0, 1, -1], [1, -1, 0], [1, 0, -1]])
)
assert set(map(tuple, sol.permuteUnique([-1, -1, 1]))) == set(
    map(tuple, [[-1, -1, 1], [-1, 1, -1], [1, -1, -1]])
)
