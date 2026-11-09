"""
EPI 16.8 Find the minimum weight path in a triangle

Given a list triangle, where row i holds i + 1 integers, return the
least sum of a path from the top to the bottom row. The path holds one
entry of each row. From entry j of a row, the path goes to entry j or
entry j + 1 of the next row. The empty triangle has least sum 0.

Example 1:

Input: triangle = [[2],
                   [3, 4],
                   [6, 5, 7],
                   [4, 1, 8, 3]]
Output: 11
Explanation: 2 + 3 + 5 + 1.

          2
        3   4
      6   5   7
    4   1   8   3

Example 2:

Input: triangle = [[1],
                   [9, 2],
                   [9, 9, 3]]
Output: 6
Explanation: 1 + 2 + 3.

Example 3:

Input: triangle = []
Output: 0

Constraints:

    0 <= len(triangle) <= 200
    len(triangle[i]) == i + 1
    -1000 <= triangle[i][j] <= 1000

    REQUIRED: O(n^2) time and O(n) extra space, where n is
    len(triangle). NO enumeration of every path.
"""


class Solution:
    def minimum_path_weight(self, triangle: list[list[int]]) -> int:
        pass


sol = Solution()

print(sol.minimum_path_weight([[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]]))  # 11

# assert sol.minimum_path_weight([[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]]) == 11
# assert sol.minimum_path_weight([[1], [9, 2], [9, 9, 3]]) == 6
# assert sol.minimum_path_weight([]) == 0
# assert sol.minimum_path_weight([[7]]) == 7
# assert sol.minimum_path_weight([[1], [2, 3]]) == 3
# assert sol.minimum_path_weight([[-1], [2, 3], [1, -1, -3]]) == -1
# assert sol.minimum_path_weight([[0], [5, 0], [5, 5, 0], [0, 5, 5, 5]]) == 5
# T = [[1], [2, 1], [3, 2, 1]]
# assert sol.minimum_path_weight(T) == 3
# assert T == [[1], [2, 1], [3, 2, 1]]
# assert sol.minimum_path_weight([[(i * 13 + j * 7) % 19 - 5 for j in range(i + 1)] for i in range(200)]) == -406
# assert sol.minimum_path_weight([[(i * 7 + j * 3) % 10 + 1 for j in range(i + 1)] for i in range(200)]) == 200
