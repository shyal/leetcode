"""
URL: https://leetcode.com/problems/permutations/description/

46. Permutations

Given an array nums of distinct integers, return all the possible permutations. You can return the answer in any order.


Example 1:
Input: nums = [1,2,3]
Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
Example 2:
Input: nums = [0,1]
Output: [[0,1],[1,0]]
Example 3:
Input: nums = [1]
Output: [[1]]


Constraints:

        1 <= nums.length <= 6
        -10 <= nums[i] <= 10
        All the integers of nums are unique.
---

Hmm i'm only getting:

[[1, 2, 3], [2, 1, 3], [2, 3, 1]]

Duh.. i was close, but had to look up the solution.

The real insight i missed on was the for loop.

                           [1,2,3]   ← dfs(0)
                          /     |     \\
                         /      |      \\
                        /       |       \\
                swap(0,0)  swap(0,1)  swap(0,2)
                   ↓          ↓          ↓
               [1,2,3]     [2,1,3]     [3,2,1]
                 |            |            |
              dfs(1)        dfs(1)       dfs(1)
              /   \\         /   \\         /   \\
             /     \\       /     \\       /     \\
      swap(1,1) swap(1,2) swap(1,1) swap(1,2) swap(1,1) swap(1,2)
         ↓         ↓         ↓         ↓         ↓         ↓
     [1,2,3]   [1,3,2]   [2,1,3]   [2,3,1]   [3,2,1]   [3,1,2]
        |         |         |         |         |         |
      dfs(2)    dfs(2)    dfs(2)    dfs(2)    dfs(2)    dfs(2)
        |         |         |         |         |         |
        ↓         ↓         ↓         ↓         ↓         ↓
     [1,2,3]   [1,3,2]   [2,1,3]   [2,3,1]   [3,2,1]   [3,1,2]
        |         |         |         |         |         |
     dfs(3)→✅  dfs(3)→✅  dfs(3)→✅  dfs(3)→✅  dfs(3)→✅  dfs(3)→✅

i is the starting index of each recursive branch (so i + 1 on the next recursion),
and we range from i to n as j.

Hard to mentally visualize.

"""


class Solution:

    def permute(self, nums: List[int]) -> List[List[int]]:
        def dfs(i):
            if i == len(nums):
                res.append(nums[:])
                return
            for j in range(i, len(nums)):
                nums[i], nums[j] = nums[j], nums[i]
                dfs(i + 1)
                nums[i], nums[j] = nums[j], nums[i]

        res = []
        dfs(0)
        return res


sol = Solution()
res = sol.permute(nums=[1, 2, 3])
# print(res)
