# REFERENCE: d360 Sudoku Solver
class Solution:
    def sudoku_solve(self, board):
        rows = [set() for _ in range(9)]
        cols = [set() for _ in range(9)]
        boxes = [set() for _ in range(9)]

        def box(i, j):
            return i // 3 * 3 + j // 3

        def free(i, j, c):
            return c not in rows[i] and c not in cols[j] and c not in boxes[box(i, j)]

        def place(i, j, c):
            rows[i].add(c)
            cols[j].add(c)
            boxes[box(i, j)].add(c)
            board[i][j] = c

        def lift(i, j, c):
            rows[i].remove(c)
            cols[j].remove(c)
            boxes[box(i, j)].remove(c)
            board[i][j] = "."

        blanks = []
        for i in range(9):
            for j in range(9):
                c = board[i][j]
                if c == ".":
                    blanks.append((i, j))
                elif not free(i, j, c):
                    return False
                else:
                    place(i, j, c)

        def fill(k):
            if k == len(blanks):
                return True
            r, col = blanks[k]
            for d in "123456789":
                if free(r, col, d):
                    place(r, col, d)
                    if fill(k + 1):
                        return True
                    lift(r, col, d)
            return False

        return fill(0)
