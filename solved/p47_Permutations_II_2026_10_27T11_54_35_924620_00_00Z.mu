# URL: https://leetcode.com/problems/permutations-ii/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 47. Permutations II
#
# Given a collection of numbers, nums, that might contain duplicates, return all possible unique permutations in any order.
#
# Example 1:
#
# Input: nums = [1,1,2]
# Output:
# [
#  [1,1,2],
#  [1,2,1],
#  [2,1,1]
# ]
#
# Example 2:
#
# Input: nums = [1,2,3]
# Output:
# [
#  [1,2,3],
#  [1,3,2],
#  [2,1,3],
#  [2,3,1],
#  [3,1,2],
#  [3,2,1]
# ]
#
# Constraints:
#
#     1 <= nums.length <= 8
#     -10 <= nums[i] <= 10
#
# ---
# LEETCODE: Accepted (168 ms, 20.5 MB)

# mu 0.13

class Solution
  def permuteUnique(nums: [int]) -> [[int]]
    ret res, path, used, seen = [].., table(len(nums), fill=False), set([])
    nums.sort()
    {
      (i) ->
        if len path == len nums and tuple(path) not in seen
          res <- path[:]
          seen.add(tuple(path[:]))
        for j in 0..<len nums
          if used[j]
            continue
          used[j] = true
          path <- nums[j]
          mu(j + 1)
          path .
          used[j] = false
    }(0)

sol = Solution()

print(sol.permuteUnique([1, 1, 2]))  # [[1,1,2],[1,2,1],[2,1,1]]

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
