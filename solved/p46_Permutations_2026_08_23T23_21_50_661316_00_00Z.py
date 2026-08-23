"""
URL: https://leetcode.com/problems/permutations/description/?envType=problem-list-v2&envId=vn57k9wr

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

Wrote this instead:

class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        def helper(i):
            if i == len(nums):
                res.append(curr[:])
                return
            for j in range(i, len(nums)):
                curr.append(nums[j])
                helper(j + 1)
                curr.pop()

        curr = []
        res = []
        helper(0)
        return res

Which is probably me confusing permutations with combinations. Had to peek at the answer.
So this is assisted / spoiled / learning.

"""


class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        def helper(i):
            if i == len(nums):
                res.append(nums[:])
            for j in range(i, len(nums)):
                nums[i], nums[j] = nums[j], nums[i]
                helper(i + 1)
                nums[i], nums[j] = nums[j], nums[i]

        res = []
        helper(0)
        print([*sorted(res)])
        return [*sorted(res)]


sol = Solution()

print(sol.permute([1, 2, 3]))  # [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]

# assert sorted(sol.permute([1, 2, 3])) == sorted(
#     [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
# )
# assert sorted(sol.permute([0, 1])) == sorted([[0, 1], [1, 0]])
# assert sol.permute([1]) == [[1]]

# assert sorted(sol.permute([1, 2])) == [[1, 2], [2, 1]]
# assert sorted(sol.permute([1])) == [[1]]
# assert sorted(sol.permute([-1, 0, 1])) == [
#     [-1, 0, 1],
#     [-1, 1, 0],
#     [0, -1, 1],
#     [0, 1, -1],
#     [1, -1, 0],
#     [1, 0, -1],
# ]
# assert sorted(sol.permute([10, -10, 0])) == [
#     [-10, 0, 10],
#     [-10, 10, 0],
#     [0, -10, 10],
#     [0, 10, -10],
#     [10, -10, 0],
#     [10, 0, -10],
# ]
# assert sorted(sol.permute([1, 2, 3, 4])) == [
#     [1, 2, 3, 4],
#     [1, 2, 4, 3],
#     [1, 3, 2, 4],
#     [1, 3, 4, 2],
#     [1, 4, 2, 3],
#     [1, 4, 3, 2],
#     [2, 1, 3, 4],
#     [2, 1, 4, 3],
#     [2, 3, 1, 4],
#     [2, 3, 4, 1],
#     [2, 4, 1, 3],
#     [2, 4, 3, 1],
#     [3, 1, 2, 4],
#     [3, 1, 4, 2],
#     [3, 2, 1, 4],
#     [3, 2, 4, 1],
#     [3, 4, 1, 2],
#     [3, 4, 2, 1],
#     [4, 1, 2, 3],
#     [4, 1, 3, 2],
#     [4, 2, 1, 3],
#     [4, 2, 3, 1],
#     [4, 3, 1, 2],
#     [4, 3, 2, 1],
# ]
# assert sorted(sol.permute([0])) == [[0]]
# assert sorted(sol.permute([1, 3, 5])) == [
#     [1, 3, 5],
#     [1, 5, 3],
#     [3, 1, 5],
#     [3, 5, 1],
#     [5, 1, 3],
#     [5, 3, 1],
# ]
# assert sorted(sol.permute([2, 4, 6, 8])) == [
#     [2, 4, 6, 8],
#     [2, 4, 8, 6],
#     [2, 6, 4, 8],
#     [2, 6, 8, 4],
#     [2, 8, 4, 6],
#     [2, 8, 6, 4],
#     [4, 2, 6, 8],
#     [4, 2, 8, 6],
#     [4, 6, 2, 8],
#     [4, 6, 8, 2],
#     [4, 8, 2, 6],
#     [4, 8, 6, 2],
#     [6, 2, 4, 8],
#     [6, 2, 8, 4],
#     [6, 4, 2, 8],
#     [6, 4, 8, 2],
#     [6, 8, 2, 4],
#     [6, 8, 4, 2],
#     [8, 2, 4, 6],
#     [8, 2, 6, 4],
#     [8, 4, 2, 6],
#     [8, 4, 6, 2],
#     [8, 6, 2, 4],
#     [8, 6, 4, 2],
# ]
