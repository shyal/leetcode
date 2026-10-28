# URL: https://leetcode.com/problems/brick-wall/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 554. Brick Wall
#
# There is a rectangular brick wall in front of you with n rows of bricks. The ith row has some number of bricks each of the same height (i.e., one unit) but they can be of different widths. The total width of each row is the same.
#
# Draw a vertical line from the top to the bottom and cross the least bricks. If your line goes through the edge of a brick, then the brick is not considered as crossed. You cannot draw a line just along one of the two vertical edges of the wall, in which case the line will obviously cross no bricks.
#
# Given the 2D array wall that contains the information about the wall, return the minimum number of crossed bricks after drawing such a vertical line.
#
# Example 1:
#
# Input: wall = [[1,2,2,1],[3,1,2],[1,3,2],[2,4],[3,1,2],[1,3,1,1]]
# Output: 2
#
# Example 2:
#
# Input: wall = [[1],[1],[1]]
# Output: 3
#
# Constraints:
#
#     n == wall.length
#     1 <= n <= 10^4
#     1 <= wall[i].length <= 10^4
#     1 <= sum(wall[i].length) <= 2 * 10^4
#     sum(wall[i]) is the same for each row i.
#     1 <= wall[i][j] <= 2^31 - 1
#
# ---
# LEETCODE: Accepted (7 ms, 22.6 MB)

# mu 0.13

class Solution
  def leastBricks(wall: [[int]]) -> int
    counts = {:int}
    for row in wall
      total = 0
      for v in row[:-1]
        total += v
        counts[total] += 1
    if not counts
      return len(wall)
    max_crosses = max(counts.items(), key= x -> x[1])[1]
    len(wall) - max_crosses


sol = Solution()

print(sol.leastBricks([[1, 2, 2, 1], [3, 1, 2], [1, 3, 2], [2, 4], [3, 1, 2], [1, 3, 1, 1]]))  # 2

assert sol.leastBricks([[1, 2, 2, 1], [3, 1, 2], [1, 3, 2], [2, 4], [3, 1, 2], [1, 3, 1, 1]]) == 2
assert sol.leastBricks([[1], [1], [1]]) == 3
assert sol.leastBricks([[1]]) == 1
assert sol.leastBricks([[1, 1, 1, 1]]) == 0
assert sol.leastBricks([[1, 2], [2, 1]]) == 1
assert sol.leastBricks([[1, 1], [1, 1], [1, 1]]) == 0
assert sol.leastBricks([[2 ** 31 - 1, 2 ** 31 - 1], [2 ** 31 - 1, 2 ** 31 - 1]]) == 0
assert sol.leastBricks([[1, 2, 3], [3, 3], [2, 4]]) == 1
assert sol.leastBricks([[1, 1, 1], [2, 1], [1, 2]]) == 1
assert sol.leastBricks([[5, 5, 5], [10, 5], [5, 10]]) == 1
assert sol.leastBricks([[1, 1, 1, 1, 1], [2, 3, 1, 1], [1, 4, 1, 1]]) == 1
assert sol.leastBricks([[1, 2, 3, 4], [3, 3, 4], [2, 5, 3]]) == 1
