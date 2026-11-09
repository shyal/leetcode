"""
EPI 15.3 Generate all nonattacking placements of n-Queens

Given n, return every way to put n queens on an n x n chessboard so that
no two queens share a row, a column or a diagonal. Write a placement as
a list p of length n, where p[r] is the column of the queen in row r.
Return the placements in any order.

Example 1:

Input: n = 4
Output: [[1, 3, 0, 2], [2, 0, 3, 1]]
Explanation: the two boards are

    . Q . .        . . Q .
    . . . Q        Q . . .
    Q . . .        . . . Q
    . . Q .        . Q . .

Example 2:

Input: n = 1
Output: [[0]]

Example 3:

Input: n = 3
Output: []
Explanation: every way to put three queens in different rows and
columns puts two of them on the same diagonal.

Constraints:

    1 <= n <= 10

    REQUIRED: O(n!) time. NO itertools.permutations. NO check of a
    board after all n queens are on it.
"""


class Solution:
    def n_queens(self, n: int) -> list[list[int]]:
        pass


sol = Solution()


def nonattacking(p):
    n = len(p)
    return (
        len(set(p)) == n
        and len({r + c for r, c in enumerate(p)}) == n
        and len({r - c for r, c in enumerate(p)}) == n
    )


print(sol.n_queens(4))  # [[1, 3, 0, 2], [2, 0, 3, 1]]

# assert sorted(sol.n_queens(4)) == [[1, 3, 0, 2], [2, 0, 3, 1]]
# assert sol.n_queens(1) == [[0]]
# assert sol.n_queens(2) == []
# assert sol.n_queens(3) == []
# assert sorted(sol.n_queens(5)) == [[0, 2, 4, 1, 3], [0, 3, 1, 4, 2], [1, 3, 0, 2, 4], [1, 4, 2, 0, 3], [2, 0, 3, 1, 4], [2, 4, 1, 3, 0], [3, 0, 2, 4, 1], [3, 1, 4, 2, 0], [4, 1, 3, 0, 2], [4, 2, 0, 3, 1]]
# assert sorted(sol.n_queens(6)) == [[1, 3, 5, 0, 2, 4], [2, 5, 1, 4, 0, 3], [3, 0, 4, 1, 5, 2], [4, 2, 0, 5, 3, 1]]
# boards = sol.n_queens(7)
# assert len(boards) == 40 and len(set(map(tuple, boards))) == 40
# assert all(len(p) == 7 and nonattacking(p) for p in boards)
# boards = sol.n_queens(8)
# assert len(boards) == 92 and len(set(map(tuple, boards))) == 92
# assert all(len(p) == 8 and nonattacking(p) for p in boards)
# assert [0, 4, 7, 5, 2, 6, 1, 3] in boards
# boards = sol.n_queens(9)
# assert len(boards) == 352 and len(set(map(tuple, boards))) == 352
# boards = sol.n_queens(10)
# assert len(boards) == 724 and len(set(map(tuple, boards))) == 724
# assert all(len(p) == 10 and nonattacking(p) for p in boards)
