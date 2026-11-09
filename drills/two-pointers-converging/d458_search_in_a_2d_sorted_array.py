"""
EPI 11.6 Search in a 2D sorted array

Given an m x n array A whose rows and columns are each sorted in
nondecreasing order, and an integer x, return True when x is in A and
False otherwise. A may be empty.

Example 1:

Input: A = [[1, 4, 7, 11],
            [2, 5, 8, 12],
            [3, 6, 9, 16],
            [10, 13, 14, 17]], x = 5
Output: True

Example 2:

Input: the same A, x = 15
Output: False

Example 3:

Input: A = [], x = 1
Output: False

Constraints:

    0 <= m, n <= 1000
    -10^9 <= A[i][j], x <= 10^9
    Each row and each column of A is sorted in nondecreasing order.

    REQUIRED: O(m + n) time, O(1) extra space. NO flattening, NO set,
    NO `in` on a row, NO bisect.
"""


class Solution:
    def matrix_search(self, A: list[list[int]], x: int) -> bool:
        pass


sol = Solution()

print(sol.matrix_search([[1, 4, 7, 11], [2, 5, 8, 12], [3, 6, 9, 16], [10, 13, 14, 17]], 5))  # True

# A = [[1, 4, 7, 11], [2, 5, 8, 12], [3, 6, 9, 16], [10, 13, 14, 17]]
# assert sol.matrix_search(A, 5) is True
# assert sol.matrix_search(A, 15) is False
# assert sol.matrix_search(A, 1) is True
# assert sol.matrix_search(A, 17) is True
# assert sol.matrix_search(A, 11) is True
# assert sol.matrix_search(A, 10) is True
# assert sol.matrix_search(A, 0) is False
# assert sol.matrix_search(A, 18) is False
# assert sol.matrix_search([], 1) is False
# assert sol.matrix_search([[]], 1) is False
# assert sol.matrix_search([[7]], 7) is True
# assert sol.matrix_search([[7]], 8) is False
# assert sol.matrix_search([[1, 3, 5]], 3) is True
# assert sol.matrix_search([[1], [3], [5]], 4) is False
# assert sol.matrix_search([[2, 2], [2, 2]], 2) is True
# B = [[i + j for j in range(1000)] for i in range(1000)]
# assert sol.matrix_search(B, 999) is True
# assert sol.matrix_search(B, 1998) is True
# assert sol.matrix_search(B, 1999) is False
# assert sol.matrix_search(B, -1) is False
