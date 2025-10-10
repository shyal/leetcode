"""
URL: https://leetcode.com/problems/search-a-2d-matrix/description/

74. Search a 2D Matrix

You are given an m x n integer matrix matrix with the following two properties:

    Each row is sorted in non-decreasing order.
    The first integer of each row is greater than the last integer of the previous row.

Given an integer target, return true if target is in matrix or false otherwise.

You must write a solution in O(log(m * n)) time complexity.

Example 1:

Input: matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3
Output: true

Example 2:

Input: matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 13
Output: false

Constraints:

    m == matrix.length
    n == matrix[i].length
    1 <= m, n <= 100
    -10^4 <= matrix[i][j], target <= 10^4

"""


class MatToList:

    def __init__(self, mat):
        self.mat = mat

    def __getitem__(self, i):
        div, mod = divmod(i, len(next(iter(self.mat), 0)))
        return self.mat[div][mod]

    def __len__(self):
        return len(self.mat) * len(next(iter(self.mat), []))


class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        mat = MatToList(matrix)
        left, right = 0, len(mat) - 1
        while left <= right:
            mid = (left + right) // 2
            val = mat[mid]
            if target == val:
                return True
            elif target < val:
                right = mid - 1
            else:
                left = mid + 1
        return False


sol = Solution()

# print(sol.searchMatrix([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 3))  # True

assert sol.searchMatrix([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 3) == True
assert sol.searchMatrix([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 13) == False
assert sol.searchMatrix([[5]], 5) == True
assert sol.searchMatrix([[5]], 4) == False
assert sol.searchMatrix([[5]], 6) == False
assert sol.searchMatrix([[1, 3, 5, 7]], 5) == True
assert sol.searchMatrix([[1, 3, 5, 7]], 0) == False
assert sol.searchMatrix([[1, 3, 5, 7]], 8) == False
assert sol.searchMatrix([[1], [3], [5], [7]], 3) == True
assert sol.searchMatrix([[1], [3], [5], [7]], 0) == False
assert sol.searchMatrix([[1], [3], [5], [7]], 8) == False
assert sol.searchMatrix([[-5, -3, -1], [0, 2, 4]], -3) == True
assert sol.searchMatrix([[-5, -3, -1], [0, 2, 4]], -6) == False
assert sol.searchMatrix([[-5, -3, -1], [0, 2, 4]], 5) == False
assert sol.searchMatrix([[1, 1, 1], [2, 2, 2]], 1) == True
assert sol.searchMatrix([[1, 1, 1], [2, 2, 2]], 2) == True
assert sol.searchMatrix([[1, 1, 1], [2, 2, 2]], 0) == False
assert sol.searchMatrix([[1, 1, 1], [2, 2, 2]], 3) == False
assert sol.searchMatrix([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 1) == True
assert sol.searchMatrix([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 60) == True
assert sol.searchMatrix([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 7) == True
assert sol.searchMatrix([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 10) == True
assert sol.searchMatrix([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 0) == False
assert sol.searchMatrix([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 61) == False
assert sol.searchMatrix([], 1) == False
assert sol.searchMatrix([[]], 1) == False
