# URL: https://leetcode.com/problems/maximum-path-score-in-a-grid/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 3742. Maximum Path Score in a Grid
#
# You are given an m x n grid where each cell contains one of the values 0, 1, or 2. You are also given an integer k.
#
# You start from the top-left corner (0, 0) and want to reach the bottom-right corner (m - 1, n - 1) by moving only right or down.
#
# Each cell contributes a specific score and incurs an associated cost, according to their cell values:
#
# - 0: adds 0 to your score and costs 0.
# - 1: adds 1 to your score and costs 1.
# - 2: adds 2 to your score and costs 1.
#
# Return the maximum score achievable without exceeding a total cost of k, or -1 if no valid path exists.
#
# Note: If you reach the last cell but the total cost exceeds k, the path is invalid.
#
# Example 1:
#
# Input: grid = [[0, 1],[2, 0]], k = 1
# Output: 2
# Explanation:
# The optimal path is:
#
# Cell      grid[i][j]  Score  Total Score  Cost  Total Cost
# (0, 0)   0           0      0            0     0
# (1, 0)   2           2      2            1     1
# (1, 1)   0           0      2            0     1
#
# Thus, the maximum possible score is 2.
#
# Example 2:
#
# Input: grid = [[0, 1],[1, 2]], k = 1
# Output: -1
# Explanation:
# There is no path that reaches cell (1, 1) without exceeding cost k. Thus, the answer is -1.
#
# Constraints:
#
#     1 <= m, n <= 200
#     0 <= k <= 10^3
#     grid[0][0] == 0
#     0 <= grid[i][j] <= 2
#
# ---
# 
# Dijstrak gets a TLE
# 
# class Solution
#   def maxPathScore(grid: [[int]], k: int) -> int
#     costf = (r, c) -> min(1, grid[r][c])
#     h = heap([(grid[0][0], costf(0, 0), 0, 0)], max)
#     seen = set([])
#     max_score = -1
#     while h
#       score, cost, r, c = h.pop()
#       if (score, cost, r, c) in seen or cost > k
#         continue
#       if (r, c) == shape(grid, last_index=true)
#         max_score = max(max_score, score)
#       seen.add((score, cost, r, c))
#       for rr, cc in [(r+1, c), (r, c+1)]
#         if in_bounds(grid, rr, cc)
#           h <- (score + grid[rr][cc], cost + costf(rr, cc), rr, cc)
#     max_score
# 
# learning
# mu 0.20

class Solution
  def maxPathScore(grid: [[int]], k: int) -> int
    k = min(k, len grid + len grid[0])
    dp = table(len grid + 1, len grid[0] + 1, k + 1, fill=-inf)
    dp[0][1][0] = 0
    for r, c in cells(dp, start=1)
      v = grid[r-1][c-1]
      s = [max(a, b) + v for a, b in zip(dp[r-1][c], dp[r][c-1])]
      dp[r][c] = v ? [-inf] + s[:-1] : s
    max(-1, max(dp[-1][-1]))
      


sol = Solution()
assert sol.maxPathScore([[0, 2, 0, 2, 0], [1, 0, 1, 0, 1], [0, 2, 0, 2, 0], [1, 0, 1, 0, 1]], 5) == 7

# print(sol.maxPathScore([[0, 1], [2, 0]], 1))  # 2

assert sol.maxPathScore([[0, 1], [2, 0]], 1) == 2
assert sol.maxPathScore([[0, 1], [1, 2]], 1) == -1
assert Solution().maxPathScore([[0]], 0) == 0
assert Solution().maxPathScore([[0, 0, 0], [0, 0, 0], [0, 0, 0]], 0) == 0
assert Solution().maxPathScore([[0, 2, 2], [2, 2, 2], [2, 2, 0]], 5) == 6
assert Solution().maxPathScore([[0, 1, 1], [1, 1, 1], [1, 1, 0]], 3) == 3
assert Solution().maxPathScore([[0, 2, 1], [1, 2, 1], [2, 1, 0]], 4) == 5
assert Solution().maxPathScore([[0] * 200 for _ in 0..<200], 0) == 0
assert Solution().maxPathScore([[0] + [2] * 199] + [[2] * 200 for _ in 0..<199], 1000) == 796
assert Solution().maxPathScore([[0] + [1] * 199] + [[1] * 200 for _ in 0..<199], 200) == -1
assert Solution().maxPathScore([[0] + [2] * 199] + [[2] * 200 for _ in 0..<199], 0) == -1
assert Solution().maxPathScore([[0, 1, 2], [2, 1, 0], [1, 0, 2]], 2) == -1
assert Solution().maxPathScore([[0, 2, 2, 2], [2, 2, 2, 2], [2, 2, 2, 0]], 3) == -1
assert Solution().maxPathScore([[0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 0]], 2) == 2
assert tle(sol.maxPathScore, 3742)
