"""
URL: https://leetcode.com/problems/maximal-rectangle/description/?envType=problem-list-v2&envId=vn57k9wr

85. Maximal Rectangle

Given a rows x cols binary matrix filled with 0's and 1's, find the largest rectangle containing only 1's and return its area.

Example 1:

Input: matrix = [["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]]
Output: 6
Explanation: The maximal rectangle is shown in the above picture.

Example 2:

Input: matrix = [["0"]]
Output: 0

Example 3:

Input: matrix = [["1"]]
Output: 1

Constraints:

    rows == matrix.length
    cols == matrix[i].length
    1 <= rows, cols <= 200
    matrix[i][j] is '0' or '1'.

---

Failed to detect this was a monotonic stack... again. This suggests i need:

1/ drill monotonic stack
2/ think of questions to ask to detect whether a monotonic stack solution applies to a question

"""


class Solution:
    def maximalRectangle(self, matrix: List[List[str]]) -> int:
        pass


sol = Solution()

print(
    sol.maximalRectangle(
        [
            ["1", "0", "1", "0", "0"],
            ["1", "0", "1", "1", "1"],
            ["1", "1", "1", "1", "1"],
            ["1", "0", "0", "1", "0"],
        ]
    )
)  # 6

# assert (
#     sol.maximalRectangle(
#         [
#             ["1", "0", "1", "0", "0"],
#             ["1", "0", "1", "1", "1"],
#             ["1", "1", "1", "1", "1"],
#             ["1", "0", "0", "1", "0"],
#         ]
#     )
#     == 6
# )
# assert sol.maximalRectangle([["0"]]) == 0
# assert sol.maximalRectangle([["1"]]) == 1

# assert sol.maximalRectangle([["0", "0", "0"], ["0", "0", "0"], ["0", "0", "0"]]) == 0
# assert sol.maximalRectangle([["1", "1", "1"], ["1", "1", "1"], ["1", "1", "1"]]) == 9
# assert (
#     sol.maximalRectangle(
#         [
#             ["1", "0", "1", "1", "1"],
#             ["1", "0", "1", "1", "1"],
#             ["1", "1", "1", "1", "1"],
#             ["1", "0", "0", "1", "0"],
#         ]
#     )
#     == 9
# )
# assert sol.maximalRectangle([["1"] * 200] * 200) == 40000
# assert sol.maximalRectangle([["0"] * 200] * 200) == 0
# assert sol.maximalRectangle([["1"] * 200]) == 200
# assert sol.maximalRectangle([["0"] * 200]) == 0
# assert sol.maximalRectangle([["1"], ["1"], ["1"], ["0"], ["1"]]) == 3
# assert sol.maximalRectangle([["1", "1", "0", "1", "1", "1", "0", "1"]]) == 3
# assert sol.maximalRectangle([["0", "1", "0", "1", "0", "1", "0", "1"]]) == 1
# assert sol.maximalRectangle([["1", "1", "1", "0", "0", "1", "1", "1", "1", "1"]]) == 5
# assert sol.maximalRectangle([["1", "0", "1", "0", "1", "0", "1", "0", "1", "0"]]) == 1


# FAILED: walked away after 20m 49s; no working solution.
# Judge the moves actually attempted as struggled, not clean.
