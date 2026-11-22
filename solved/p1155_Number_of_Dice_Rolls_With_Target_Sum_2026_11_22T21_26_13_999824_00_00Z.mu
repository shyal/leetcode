# URL: https://leetcode.com/problems/number-of-dice-rolls-with-target-sum/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 1155. Number of Dice Rolls With Target Sum
#
# You have n dice, and each dice has k faces numbered from 1 to k.
#
# Given three integers n, k, and target, return the number of possible ways (out of the k^n total ways) to roll the dice, so the sum of the face-up numbers equals target. Since the answer may be too large, return it modulo 10^9 + 7.
#
# Example 1:
#
# Input: n = 1, k = 6, target = 3
# Output: 1
# Explanation: You throw one die with 6 faces.
# There is only one way to get a sum of 3.
#
# Example 2:
#
# Input: n = 2, k = 6, target = 7
# Output: 6
# Explanation: You throw two dice, each with 6 faces.
# There are 6 ways to get a sum of 7: 1+6, 2+5, 3+4, 4+3, 5+2, 6+1.
#
# Example 3:
#
# Input: n = 30, k = 30, target = 500
# Output: 222616187
# Explanation: The answer must be returned modulo 10^9 + 7.
#
# Constraints:
#
#     1 <= n, k <= 30
#     1 <= target <= 1000
#
# ---
# 
# brute force:
# 
# class Solution
#   def numRollsToTarget(n: int, k: int, target: int) -> int
#     def helper(i, total)
#       if len path == n and total == target
#         res <- tuple(path[:])
#       for j in i..<len(arr)
#         path <- arr[j]
#         helper(i+1, total + arr[j])
#         path .
#     arr = [*1..k] * n
#     res, path = []..
#     helper(0, 0)
#     len set(res)
# Learning
# mu 0.20

class Solution
  def numRollsToTarget(n: int, k: int, target: int) -> int
    memo ways(d, t) -> d == 0: t == 0
                    -> t < 0: 0
        (sum for face in 1..k: ways(d - 1, t - face)) % MOD
    ways(n, target)

sol = Solution()

print(sol.numRollsToTarget(1, 6, 3))  # 1

assert sol.numRollsToTarget(1, 6, 3) == 1
assert sol.numRollsToTarget(2, 6, 7) == 6
assert sol.numRollsToTarget(30, 30, 500) == 222616187

assert sol.numRollsToTarget(1, 1, 1) == 1
assert sol.numRollsToTarget(1, 1, 2) == 0
assert sol.numRollsToTarget(2, 1, 2) == 1
assert sol.numRollsToTarget(2, 1, 3) == 0
assert sol.numRollsToTarget(2, 2, 3) == 2
assert sol.numRollsToTarget(3, 2, 6) == 1
assert sol.numRollsToTarget(3, 2, 7) == 0
assert sol.numRollsToTarget(30, 1, 30) == 1
assert sol.numRollsToTarget(30, 1, 31) == 0
assert sol.numRollsToTarget(30, 30, 900) == 1
assert sol.numRollsToTarget(30, 30, 1000) == 0
assert sol.numRollsToTarget(30, 30, 30) == 1
