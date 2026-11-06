"""
Given a 2D list binaryMatrix of 0s and 1s, return the number of
islands. An island is a group of cells holding 1 in which every cell
can reach every other cell of the group through cells of the group
that share a side. Two cells that share only a corner are not
connected.

Example 1:

Input: binaryMatrix = [[0, 1, 0, 1, 0],
                       [0, 0, 1, 1, 1],
                       [1, 0, 0, 1, 0],
                       [0, 1, 1, 0, 0],
                       [1, 0, 1, 0, 1]]
Output: 6
Explanation: the 1 at row 0, column 1 is an island on its own. It
touches the 1 at row 1, column 2 only at a corner. The four cells at
rows 3 and 4, columns 1 and 2, are one island, and so are the five 1s
at the top right.

Example 2:

Input: binaryMatrix = [[1, 0, 1, 0]]
Output: 2

Example 3:

Input: binaryMatrix = [[0]]
Output: 0

Constraints:

    1 <= len(binaryMatrix) <= 100
    1 <= len(binaryMatrix[0]) <= 100
    binaryMatrix[i][j] is 0 or 1.
    binaryMatrix may be changed.

    REQUIRED: O(rows * cols) time. NO union-find, NO recursion.
"""


class Solution:
    def get_number_of_islands(self, binaryMatrix: list[list[int]]) -> int:
        pass


sol = Solution()

print(sol.get_number_of_islands([[0, 1, 0, 1, 0], [0, 0, 1, 1, 1], [1, 0, 0, 1, 0], [0, 1, 1, 0, 0], [1, 0, 1, 0, 1]]))  # 6

# assert sol.get_number_of_islands([[0, 1, 0, 1, 0], [0, 0, 1, 1, 1], [1, 0, 0, 1, 0], [0, 1, 1, 0, 0], [1, 0, 1, 0, 1]]) == 6
# assert sol.get_number_of_islands([[1, 0, 1, 0]]) == 2
# assert sol.get_number_of_islands([[0]]) == 0
# assert sol.get_number_of_islands([[1]]) == 1
# assert sol.get_number_of_islands([[1, 0, 1, 0], [0, 1, 1, 1], [0, 0, 1, 0]]) == 2
# assert sol.get_number_of_islands([[1, 0, 1, 0], [0, 1, 1, 1], [0, 0, 1, 0], [1, 1, 0, 0], [0, 1, 0, 1]]) == 4
# assert sol.get_number_of_islands([[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1]]) == 1
# assert sol.get_number_of_islands([[1], [1], [0], [1]]) == 2
# assert sol.get_number_of_islands([[1, 0], [0, 1]]) == 2
# assert sol.get_number_of_islands([[0] * 100 for _ in range(100)]) == 0
# assert sol.get_number_of_islands([[1] * 100 for _ in range(100)]) == 1
# assert sol.get_number_of_islands([[(i + j) % 2 for j in range(100)] for i in range(100)]) == 5000
# assert sol.get_number_of_islands([[1 if i % 2 == 0 else 0] * 100 for i in range(100)]) == 50
# assert sol.get_number_of_islands([[1 if j % 2 == 0 else 0 for j in range(100)] for i in range(100)]) == 50
