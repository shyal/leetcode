"""
URL: https://leetcode.com/problems/count-negative-numbers-in-a-sorted-matrix/description/?envType=problem-list-v2&envId=vn57k9wr

1351. Count Negative Numbers in a Sorted Matrix

Given a m x n matrix grid which is sorted in non-increasing order both row-wise and column-wise, return the number of negative numbers in grid.

Example 1:

Input: grid = [[4,3,2,-1],[3,2,1,-1],[1,1,-1,-2],[-1,-1,-2,-3]]
Output: 8
Explanation: There are 8 negatives number in the matrix.

Example 2:

Input: grid = [[3,2],[1,0]]
Output: 0

Constraints:

    m == grid.length
    n == grid[i].length
    1 <= m, n <= 100
    -100 <= grid[i][j] <= 100

Follow up: Could you find an O(n + m) solution?
"""


class Solution:
    def countNegatives(self, grid: List[List[int]]) -> int:
        count = 0
        for i in range(len(grid) - 1, -1, -1):
            for j in range(len(grid[i]) - 1, -1, -1):
                if grid[i][j] < 0:
                    count += 1
                else:
                    break
        return count


sol = Solution()

# print(
#     sol.countNegatives([[4, 3, 2, -1], [3, 2, 1, -1], [1, 1, -1, -2], [-1, -1, -2, -3]])
# )  # 8

assert (
    sol.countNegatives([[4, 3, 2, -1], [3, 2, 1, -1], [1, 1, -1, -2], [-1, -1, -2, -3]])
    == 8
)
assert sol.countNegatives([[3, 2], [1, 0]]) == 0
assert sol.countNegatives([[-5]]) == 1
assert sol.countNegatives([[5]]) == 0
assert sol.countNegatives([[0]]) == 0
assert sol.countNegatives([[3, 2, 1]]) == 0
assert sol.countNegatives([[3, 2, -1, -2]]) == 2
assert sol.countNegatives([[3], [2], [1]]) == 0
assert sol.countNegatives([[3], [2], [-1], [-2]]) == 2
assert sol.countNegatives([[-1, -2], [-3, -4]]) == 4
assert sol.countNegatives([[4, 3], [2, 1]]) == 0
assert sol.countNegatives([[1, 0, 0], [0, 0, -1], [-1, -1, -2]]) == 4
assert sol.countNegatives([]) == 0
assert sol.countNegatives([[]]) == 0
