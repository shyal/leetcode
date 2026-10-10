"""
URL: https://leetcode.com/problems/battleships-in-a-board/description/?envType=problem-list-v2&envId=vn57k9wr

419. Battleships in a Board

Given an m x n matrix board where each cell is a battleship 'X' or empty '.' , return the number of the battleships on board.

Battleships can only be placed horizontally or vertically on board. In other words, they can only be made of the shape 1 x k (1 row, k columns) or k x 1 (k rows, 1 column), where k can be of any size. At least one horizontal or vertical cell separates between two battleships (i.e., there are no adjacent battleships).

Example 1:

Input: board = [["X",".",".","X"],[".",".",".","X"],[".",".",".","X"]]
Output: 2

Example 2:

Input: board = [["."]]
Output: 0

Constraints:

    m == board.length
    n == board[i].length
    1 <= m, n <= 200
    board[i][j] is either '.' or 'X'.

Follow up: Could you do it in one-pass, using only O(1) extra memory and without modifying the values board?
---
poorly worded questions. This is number of islands.

So we can iterate over the board, and explore the neighours by tagging them.

[["X",".",".","X"],
 [".",".",".","X"],
 [".",".",".","X"]]

[["0",".",".","X"],
 [".",".",".","X"],
 [".",".",".","X"]]

[["0",".",".","1"],
 [".",".",".","1"],
 [".",".",".","1"]]

for example, we could tag our first exploration as 0, and our second as 1

LEETCODE: Accepted (7 ms, 21.5 MB)
"""


# mu 0.7
# def countBattleships(board: [[str]]) -> int
#   def explore(i, j, tag)
#     board[i][j] = tag
#     for (ii, jj) in nbrs(board, i, j, eq='X')
#       explore(ii, jj, tag)
#   tag = 0
#   ret count = 0
#   for (i, j) in cells(board, eq='X')
#     if board[i][j] == 'X'
#       count += 1
#     explore(i, j, tag)
#     tag += 1
#   # tabulate(board)

def _holds(v, eq=None, lt=None, lte=None, gt=None, gte=None):
    return (
        (eq is None or v == eq)
        and (lt is None or v < lt)
        and (lte is None or v <= lte)
        and (gt is None or v > gt)
        and (gte is None or v >= gte)
    )


CARDINALS = ((-1, 0), (0, -1), (0, 1), (1, 0))


def nbrs(
    grid, r, c=None, dirs=CARDINALS, val=None, eq=None, lt=None, lte=None, gt=None, gte=None
):
    """On-grid cells next to (r, c): up, left, right, down. nbrs(grid, p)
    takes the cell as one pair. With eq, lt, lte, gt or gte, only the cells
    whose value passes them all. val is the old name for eq."""
    if c is None:
        r, c = r
    eq = val if eq is None else eq
    row = list.__getitem__ if isinstance(grid, list) else lambda g, i: g[i]
    m, n = len(grid), len(row(grid, 0))
    if dirs is CARDINALS:
        out = []
        if r > 0:
            out.append((r - 1, c))
        if c > 0:
            out.append((r, c - 1))
        if c + 1 < n:
            out.append((r, c + 1))
        if r + 1 < m:
            out.append((r + 1, c))
    else:
        out = [(r + dr, c + dc) for dr, dc in dirs if 0 <= r + dr < m and 0 <= c + dc < n]
    if eq is None and lt is None and lte is None and gt is None and gte is None:
        return out
    return [(i, j) for i, j in out if _holds(row(grid, i)[j], eq, lt, lte, gt, gte)]


def cells(grid, start=0, val=None, eq=None, lt=None, lte=None, gt=None, gte=None):
    eq = val if eq is None else eq
    for i in range(start, len(grid)):
        for j in range(start, len(grid[0])):
            if _holds(grid[i][j], eq, lt, lte, gt, gte):
                yield i, j


class Grid(list):
    """A list of rows that also takes a (row, col) pair as an index."""

    def __getitem__(self, k):
        if type(k) is tuple:
            return list.__getitem__(self, k[0])[k[1]]
        return list.__getitem__(self, k)

    def __setitem__(self, k, v):
        if type(k) is tuple:
            list.__getitem__(self, k[0])[k[1]] = v
        else:
            list.__setitem__(self, k, v)


class Solution:
    def countBattleships(self, board: list[list[str]]) -> int:
        _in_board, board = board, Grid(board)
        _w_board = board
        try:
            def explore(i, j, tag):
                board[i][j] = tag
                for (ii, jj) in nbrs(board, i, j, eq='X'):
                    explore(ii, jj, tag)
            tag = 0
            count = 0
            for (i, j) in cells(board, eq='X'):
                if board[i][j] == 'X':
                    count += 1
                explore(i, j, tag)
                tag += 1
            return count
        finally:
            _in_board[:] = _w_board


sol = Solution()
print(sol.countBattleships([['X', '.', '.', 'X'], ['.', '.', '.', 'X'], ['.', '.', '.', 'X']]))
_l, _r = sol.countBattleships([['X', '.', '.', 'X'], ['.', '.', '.', 'X'], ['.', '.', '.', 'X']]), 2
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.countBattleships([['.']]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.countBattleships([['X']]), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.countBattleships([['.']]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.countBattleships([['X', 'X', 'X', 'X']]), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.countBattleships([['X'], ['X'], ['X'], ['X']]), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.countBattleships([['X', '.', 'X', '.', 'X']]), 3
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.countBattleships([['X'], ['.'], ['X'], ['.'], ['X']]), 3
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.countBattleships([['X' if (i + j) % 2 == 0 else '.' for j in range(0, 200)] for i in range(0, 200)]), 20000
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.countBattleships([['X'] + ['.'] * 199]), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.countBattleships([['.'] * 199 + ['X']]), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.countBattleships([['X']] + [['.'] * 200 for _ in range(0, 199)]), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
