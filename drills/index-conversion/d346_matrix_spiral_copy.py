"""
Given a matrix of integers inputMatrix, return its values as one list in
clockwise spiral order: the top row left to right, the right column top
to bottom, the bottom row right to left, the left column bottom to top,
then the same for the matrix that is left inside.

Example 1:

Input: inputMatrix = [[1, 2, 3, 4, 5],
                      [6, 7, 8, 9, 10]]
Output: [1, 2, 3, 4, 5, 10, 9, 8, 7, 6]
Explanation: after the top row and the right column, the bottom row is
read right to left. There is no left column left to read.

Example 2:

Input: inputMatrix = [[1, 2, 3, 4, 5],
                      [6, 7, 8, 9, 10],
                      [11, 12, 13, 14, 15],
                      [16, 17, 18, 19, 20]]
Output: [1, 2, 3, 4, 5, 10, 15, 20, 19, 18, 17, 16, 11, 6, 7, 8, 9, 14, 13, 12]

Example 3:

Input: inputMatrix = [[1], [2]]
Output: [1, 2]

Constraints:

    1 <= len(inputMatrix) <= 100
    1 <= len(inputMatrix[0]) <= 100
    Every row has the same length.

    REQUIRED: O(rows * cols) time. NO table of visited cells, NO
    rotation of the matrix.
"""


class Solution:
    def spiral_copy(self, inputMatrix: list[list[int]]) -> list[int]:
        pass


sol = Solution()

print(sol.spiral_copy([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]))  # [1, 2, 3, 4, 5, 10, 9, 8, 7, 6]

# assert sol.spiral_copy([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]) == [1, 2, 3, 4, 5, 10, 9, 8, 7, 6]
# assert sol.spiral_copy([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15], [16, 17, 18, 19, 20]]) == [1, 2, 3, 4, 5, 10, 15, 20, 19, 18, 17, 16, 11, 6, 7, 8, 9, 14, 13, 12]
# assert sol.spiral_copy([[1], [2]]) == [1, 2]
# assert sol.spiral_copy([[1]]) == [1]
# assert sol.spiral_copy([[1, 2]]) == [1, 2]
# assert sol.spiral_copy([[1, 2], [3, 4]]) == [1, 2, 4, 3]
# assert sol.spiral_copy([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == [1, 2, 3, 6, 9, 8, 7, 4, 5]
# assert sol.spiral_copy([[1, 2, 3], [4, 5, 6]]) == [1, 2, 3, 6, 5, 4]
# assert sol.spiral_copy([[1, 2], [3, 4], [5, 6]]) == [1, 2, 4, 6, 5, 3]
# assert sol.spiral_copy([[1], [2], [3], [4]]) == [1, 2, 3, 4]
# assert sol.spiral_copy([[1, 2, 3, 4]]) == [1, 2, 3, 4]
# assert sol.spiral_copy([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]) == [1, 2, 3, 6, 9, 12, 11, 10, 7, 4, 5, 8]
# assert sol.spiral_copy([[r * 100 + c for c in range(100)] for r in range(100)])[:102] == list(range(100)) + [199, 299]
# assert len(sol.spiral_copy([[r * 100 + c for c in range(100)] for r in range(100)])) == 10000
