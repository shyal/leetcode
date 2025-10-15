"""
URL: https://leetcode.com/problems/search-a-2d-matrix-ii/description/

240. Search a 2D Matrix II

Write an efficient algorithm that searches for a value target in an m x n integer matrix matrix. This matrix has the following properties:

        Integers in each row are sorted in ascending from left to right.
        Integers in each column are sorted in ascending from top to bottom.


Example 1:

Input: matrix = [[1,4,7,11,15],[2,5,8,12,19],[3,6,9,16,22],[10,13,14,17,24],[18,21,23,26,30]], target = 5
Output: true

Example 2:

Input: matrix = [[1,4,7,11,15],[2,5,8,12,19],[3,6,9,16,22],[10,13,14,17,24],[18,21,23,26,30]], target = 20
Output: false


Constraints:

        m == matrix.length
        n == matrix[i].length
        1 <= n, m <= 300
        -109 <= matrix[i][j] <= 109
        All the integers in each row are sorted in ascending order.
        All the integers in each column are sorted in ascending order.
        -109 <= target <= 109

---

Ok this seems pretty straight forward: serach for which row the entry
might be in, this can be done by doing a bisect of the first
column.

So the first column is: [1, 2, 3, 10, 18]
at indices:              0, 1, 2, 3, 4


>>> bisect_left([1, 2, 3, 10, 18], 0)
0

>>> bisect_right([1, 2, 3, 10, 18], 0)
0

>>> bisect_left([1, 2, 3, 10, 18], 5)
3

>>> bisect_right([1, 2, 3, 10, 18], 5)
3

>>> bisect_left([1, 2, 3, 10, 18], 30)
5

>>> bisect_right([1, 2, 3, 10, 18], 30)
5

I'm trying to decide whether to use bisect left, or right. Might be better to get bisect_left - 1


>>> bisect_left([1, 2, 3, 10, 18], 0) - 1
-1

It's useful to know we're out of bounds.

>>> bisect_left([1, 2, 3, 10, 18], 5) -1
2

Hmm no wait, this won't work because even though we get row 2, target is actually in row 1.
So bisecting the first column won't work.

We need to use the dual constraint of rows and column being sorted.

So if the number is greater than row[0] and smaller than row[-1], we can search that row.
In the case of 5, that gives us rows: 0, 1, 2.

Then we can use the column constraint to find the column. Using bisect again, if we do a
bisect right of the first row, we should get the column.

>>> bisect_left([1, 4, 7, 11, 15], 5) -1
1

This potentially gives us a column, but again, not really, because 5 could be some place else
while maintaining that constraint. So bisect isn't going to work.

Ok so with binary search, we can exclude rows and columns from the search. If target is smaller
than the first item in a row, then we can discard the rows that are greater from the search.

So i think we can only achieve range reduction.. then we'll have to search a bunch of rows and columns.

Ok got it in the end. Kind of painful, and the code isn't super clean. Also bisect isn't as efficient
as doing a bs by hand, because of array slicing.

Super interesting problem nevertheless.

"""


class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        max_row = bisect_right([x[0] for x in matrix], target)
        if max_row < 0:
            max_row = 0
        if max_row >= len(matrix):
            max_row = len(matrix) - 1
        max_col = bisect_right(matrix[0], target)
        if max_col < 0:
            max_col = 0
        if max_col >= len(matrix[0]):
            max_col = len(matrix[0]) - 1
        for r in range(max_row + 1):
            ind = bisect_left(matrix[r][:max_col], target)
            if 0 <= ind < len(matrix[r]):
                if matrix[r][ind] == target:
                    return True
        return False


assert (
    Solution().searchMatrix(
        [
            [1, 4, 7, 11, 15],
            [2, 5, 8, 12, 19],
            [3, 6, 9, 16, 22],
            [10, 13, 14, 17, 24],
            [18, 21, 23, 26, 30],
        ],
        5,
    )
    == True
)
assert (
    Solution().searchMatrix(
        [
            [1, 4, 7, 11, 15],
            [2, 5, 8, 12, 19],
            [3, 6, 9, 16, 22],
            [10, 13, 14, 17, 24],
            [18, 21, 23, 26, 30],
        ],
        20,
    )
    == False
)
assert (
    Solution().searchMatrix(
        [
            [1, 4, 7, 11, 15],
            [2, 5, 8, 12, 19],
            [3, 6, 9, 16, 22],
            [10, 13, 14, 17, 24],
            [18, 21, 23, 26, 30],
        ],
        15,
    )
    == True
)
assert (
    Solution().searchMatrix(
        [
            [1, 4, 7, 11, 15],
            [2, 5, 8, 12, 19],
            [3, 6, 9, 16, 22],
            [10, 13, 14, 17, 24],
            [18, 21, 23, 26, 30],
        ],
        30,
    )
    == True
)

assert (
    Solution().searchMatrix(
        [
            [1, 4, 7, 11, 15],
            [2, 5, 8, 12, 19],
            [3, 6, 9, 16, 22],
            [10, 13, 14, 17, 24],
            [18, 21, 23, 26, 30],
        ],
        18,
    )
    == True
)
assert (
    Solution().searchMatrix(
        [
            [1, 4, 7, 11, 15],
            [2, 5, 8, 12, 19],
            [3, 6, 9, 16, 22],
            [10, 13, 14, 17, 24],
            [18, 21, 23, 26, 30],
        ],
        1,
    )
    == True
)
assert (
    Solution().searchMatrix(
        [
            [1, 4, 7, 11, 15],
            [2, 5, 8, 12, 19],
            [3, 6, 9, 16, 22],
            [10, 13, 14, 17, 24],
            [18, 21, 23, 26, 30],
        ],
        0,
    )
    == False
)
assert (
    Solution().searchMatrix(
        [
            [1, 4, 7, 11, 15],
            [2, 5, 8, 12, 19],
            [3, 6, 9, 16, 22],
            [10, 13, 14, 17, 24],
            [18, 21, 23, 26, 30],
        ],
        31,
    )
    == False
)
assert (
    Solution().searchMatrix(
        [
            [1, 4, 7, 11, 15],
            [2, 5, 8, 12, 19],
            [3, 6, 9, 16, 22],
            [10, 13, 14, 17, 24],
            [18, 21, 23, 26, 30],
        ],
        14,
    )
    == True
)
assert (
    Solution().searchMatrix(
        [
            [1, 4, 7, 11, 15],
            [2, 5, 8, 12, 19],
            [3, 6, 9, 16, 22],
            [10, 13, 14, 17, 24],
            [18, 21, 23, 26, 30],
        ],
        25,
    )
    == False
)
assert Solution().searchMatrix([[5]], 5) == True
assert Solution().searchMatrix([[5]], 6) == False
assert Solution().searchMatrix([[1, 2, 3, 4, 5]], 3) == True
assert Solution().searchMatrix([[1, 2, 3, 4, 5]], 0) == False
assert Solution().searchMatrix([[1, 2, 3, 4, 5]], 6) == False
assert Solution().searchMatrix([[1], [2], [3], [4], [5]], 3) == True
assert Solution().searchMatrix([[1], [2], [3], [4], [5]], 0) == False
assert Solution().searchMatrix([[1], [2], [3], [4], [5]], 6) == False
assert Solution().searchMatrix([[-5]], -5) == True
assert Solution().searchMatrix([[-5]], -6) == False
assert Solution().searchMatrix([[-1, 3]], -1) == True
assert Solution().searchMatrix([[-1, 3]], 3) == True
assert Solution().searchMatrix([[-1, 3]], 0) == False
assert Solution().searchMatrix([[1, 2], [3, 4]], 4) == True
assert Solution().searchMatrix([[1, 2], [3, 4]], 5) == False
assert Solution().searchMatrix([[1, 2], [3, 4]], 0) == False
assert Solution().searchMatrix([[1, 2], [3, 4]], 2) == True
assert Solution().searchMatrix([[-10, -8], [-5, -3]], -8) == True
assert Solution().searchMatrix([[-10, -8], [-5, -3]], -10) == True
assert Solution().searchMatrix([[-10, -8], [-5, -3]], -3) == True
assert Solution().searchMatrix([[-10, -8], [-5, -3]], -4) == False
assert Solution().searchMatrix([[1, 1], [1, 1]], 1) == True
assert Solution().searchMatrix([[1, 1], [1, 1]], 2) == False
assert Solution().searchMatrix([[1, 1, 1], [1, 2, 3], [1, 4, 5]], 1) == True
assert Solution().searchMatrix([[1, 1, 1], [1, 2, 3], [1, 4, 5]], 4) == True
assert Solution().searchMatrix([[1, 1, 1], [1, 2, 3], [1, 4, 5]], 0) == False
assert Solution().searchMatrix([[1, 1, 1], [1, 2, 3], [1, 4, 5]], 6) == False
