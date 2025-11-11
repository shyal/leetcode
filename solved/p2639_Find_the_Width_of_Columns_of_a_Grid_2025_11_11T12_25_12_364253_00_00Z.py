"""
URL: https://leetcode.com/problems/find-the-width-of-columns-of-a-grid/description/?envType=problem-list-v2&envId=vn57k9wr

2639. Find the Width of Columns of a Grid

You are given a 0-indexed m x n integer matrix grid. The width of a column is the maximum length of its integers.

- For example, if grid = [[-10], [3], [12]], the width of the only column is 3 since -10 is of length 3.

Return an integer array ans of size n where ans[i] is the width of the i-th column.

The length of an integer x with len digits is equal to len if x is non-negative, and len + 1 otherwise.

Example 1:

Input: grid = [[1],[22],[333]]
Output: [3]
Explanation: In the 0th column, 333 is of length 3.

Example 2:

Input: grid = [[-15,1,3],[15,7,12],[5,6,-2]]
Output: [3,1,2]
Explanation:
In the 0th column, only -15 is of length 3.
In the 1st column, all integers are of length 1.
In the 2nd column, both 12 and -2 are of length 2.

Constraints:

    m == grid.length
    n == grid[i].length
    1 <= m, n <= 100
    -10^9 <= grid[r][c] <= 10^9
"""


class Solution:

    def getWidth(self, x):
        if x == 0:
            x = 1
        nums = floor(log10(abs(x))) + 1
        if x < 0:
            nums += 1
        return nums

    def findColumnWidth(self, grid: List[List[int]]) -> List[int]:
        res = []
        for col in range(len(next(iter(grid), []))):
            max_width = max(self.getWidth(grid[row][col]) for row in range(len(grid)))
            res.append(max_width)
        return res


sol = Solution()


assert sol.getWidth(10) == 2
assert sol.getWidth(1) == 1
assert sol.getWidth(-1) == 2
assert sol.getWidth(-10) == 3

# print(sol.findColumnWidth([[1], [22], [333]]))  # [3]

assert sol.findColumnWidth([[1], [22], [333]]) == [3]
assert sol.findColumnWidth([[-15, 1, 3], [15, 7, 12], [5, 6, -2]]) == [3, 1, 2]
assert sol.findColumnWidth([[0]]) == [1]
assert sol.findColumnWidth([[-1]]) == [2]
assert sol.findColumnWidth([[1000000000]]) == [10]
assert sol.findColumnWidth([[-1000000000]]) == [11]
assert sol.findColumnWidth([[-1000000000, 1000000000]]) == [11, 10]
assert sol.findColumnWidth([[1, 2], [3, 4], [5, 6]]) == [1, 1]
assert sol.findColumnWidth([[-10, 10], [-100, 100]]) == [4, 3]
assert sol.findColumnWidth([]) == []
assert sol.findColumnWidth([[]]) == []
