# Given a matrix of integers arr, return True when every diagonal that runs
# from top left to bottom right holds one value only, and False otherwise.
#
# Example 1:
#
# Input: arr = [[1, 2, 3, 4],
#               [5, 1, 9, 3],
#               [6, 5, 1, 2]]
# Output: False
# Explanation: the diagonal that starts at the 2 in the top row holds 2, 9,
# 2.
#
# Example 2:
#
# Input: arr = [[1, 2, 3, 4],
#               [5, 1, 2, 3],
#               [6, 5, 1, 2]]
# Output: True
# Explanation: the diagonals hold 6; 5, 5; 1, 1, 1; 2, 2, 2; 3, 3; 4.
#
# Example 3:
#
# Input: arr = [[6, 4, 4]]
# Output: True
# Explanation: each diagonal is one cell.
#
# Constraints:
#
#     1 <= len(arr) <= 20
#     1 <= len(arr[0]) <= 20
#     0 <= arr[i][j] <= 20
#     Every row has the same length.
#
#     REQUIRED: O(rows * cols) time, O(1) extra space. NO list of the
#     values of a diagonal.
#
# ---

# mu 0.17

class Solution
  def isToeplitz(arr: [[int]]) -> bool
    ret is_top = true
    for r, c in cells(arr, start=1)
      is_top &= arr[r][c] == arr[r-1][c-1]


sol = Solution()

print(sol.isToeplitz([[1, 2, 3, 4], [5, 1, 9, 3], [6, 5, 1, 2]]))  # False

assert sol.isToeplitz([[1, 2, 3, 4], [5, 1, 9, 3], [6, 5, 1, 2]]) is false
assert sol.isToeplitz([[1, 2, 3, 4], [5, 1, 2, 3], [6, 5, 1, 2]]) is true
assert sol.isToeplitz([[6, 4, 4]]) is true
assert sol.isToeplitz([[4, 0], [9, 4]]) is true
assert sol.isToeplitz([[3], [5], [6]]) is true
assert sol.isToeplitz([[3, 9], [5, 3], [6, 5]]) is true
assert sol.isToeplitz([[3, 1, 7], [4, 1, 1], [2, 4, 3]]) is false
assert sol.isToeplitz([[8, 8, 8, 8, 8], [8, 8, 8, 8, 9], [8, 8, 8, 8, 8], [8, 8, 8, 8, 8], [8, 8, 8, 8, 8]]) is false
assert sol.isToeplitz([[7]]) is true
assert sol.isToeplitz([[1, 2], [2, 2]]) is false
assert sol.isToeplitz([[1, 2], [3, 1]]) is true
assert sol.isToeplitz([[(c - r) % 21 for c in 0..<20] for r in 0..<20]) is true
assert sol.isToeplitz([[(c - r) % 21 for c in 0..<20] for r in 0..<19] + [[(c - 19) % 21 for c in 0..<19] + [1]]) is false
