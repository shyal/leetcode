# URL: https://leetcode.com/problems/climbing-stairs-ii/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 3693. Climbing Stairs II
#
# You are climbing a staircase with n + 1 steps, numbered from 0 to n.
#
# You are also given a 1-indexed integer array costs of length n, where costs[i] is the cost of step i.
#
# From step i, you can jump only to step i + 1, i + 2, or i + 3. The cost of jumping from step i to step j is defined as: costs[j] + (j - i)^2
#
# You start from step 0 with cost = 0.
#
# Return the minimum total cost to reach step n.
#
# Example 1:
#
# Input: n = 4, costs = [1,2,3,4]
# Output: 13
# Explanation:
# One optimal path is 0 -> 1 -> 2 -> 4
#
# Jump      Cost Calculation               Cost
# 0 -> 1    costs[1] + (1 - 0)^2 = 1 + 1  2
# 1 -> 2    costs[2] + (2 - 1)^2 = 2 + 1  3
# 2 -> 4    costs[4] + (4 - 2)^2 = 4 + 4  8
#
# Thus, the minimum total cost is 2 + 3 + 8 = 13
#
# Example 2:
#
# Input: n = 4, costs = [5,1,6,2]
# Output: 11
# Explanation:
# One optimal path is 0 -> 2 -> 4
#
# Jump      Cost Calculation               Cost
# 0 -> 2    costs[2] + (2 - 0)^2 = 1 + 4  5
# 2 -> 4    costs[4] + (4 - 2)^2 = 2 + 4  6
#
# Thus, the minimum total cost is 5 + 6 = 11
#
# Example 3:
#
# Input: n = 3, costs = [9,8,3]
# Output: 12
# Explanation:
# The optimal path is 0 -> 3 with total cost = costs[3] + (3 - 0)^2 = 3 + 9 = 12
#
# Constraints:
#
#     1 <= n == costs.length <= 10^5
#     1 <= costs[i] <= 10^4
#
# ---
# STAGE 1 of 3 - the approach. Write it in plain English under this line. Then run make solved.
# Dijkstra
# STAGE 1: pass
# STAGE 2 of 3 - the pseudocode. Write one comment line for each step in the solve below. Then run make solved.
# LEETCODE: Accepted (6888 ms, 38.4 MB)

# mu 0.18

class Solution
  def climbStairs(n: int, costs: [int]) -> int
    costs = [0] + costs
    q = heap([[costs[0], 0]])
    seen = set([])
    while q
      cost, step = q.pop()
      if step in seen
        continue
      if step == n
        return cost
      seen.add(step)
      for next in [step + 1, step + 2, step + 3]
        if next <= n
          q.push([cost + costs[next] + (next - step) ** 2, next])

sol = Solution()

print(sol.climbStairs(4, [1, 2, 3, 4]))  # 13

assert sol.climbStairs(4, [1, 2, 3, 4]) == 13
assert sol.climbStairs(4, [5, 1, 6, 2]) == 11
assert sol.climbStairs(3, [9, 8, 3]) == 12
assert sol.climbStairs(1, [10]) == 11
assert sol.climbStairs(2, [1, 1]) == 4
assert sol.climbStairs(3, [0, 0, 0]) == 3
assert sol.climbStairs(5, [1, 10000, 1, 10000, 1]) == 12
assert sol.climbStairs(6, [10000, 10000, 10000, 10000, 10000, 10000]) == 20018
assert sol.climbStairs(7, [1, 1, 1, 1, 1, 1, 1]) == 14
assert sol.climbStairs(4, [2, 2, 2, 2]) == 12
assert sol.climbStairs(10, [i for i in 1..<11]) == 48
assert sol.climbStairs(10, [10] * 10) == 66
assert sol.climbStairs(10, [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]) == 45
assert sol.climbStairs(3, [1, 10000, 1]) == 7
assert sol.climbStairs(100000, [1] * 100000) == 200000
