# REFERENCE: d506 EPI 15.10 Implement a Sudoku solver
class Solution:
    def solve_sudoku(self, partial_assignment):
        board = partial_assignment
        rows = [set() for _ in range(9)]
        cols = [set() for _ in range(9)]
        boxes = [set() for _ in range(9)]
        blanks = []
        for i in range(9):
            for j in range(9):
                d = board[i][j]
                if d == 0:
                    blanks.append((i, j))
                    continue
                b = i // 3 * 3 + j // 3
                if d in rows[i] or d in cols[j] or d in boxes[b]:
                    return False
                rows[i].add(d)
                cols[j].add(d)
                boxes[b].add(d)

        def fill(k):
            if k == len(blanks):
                return True
            r, c = blanks[k]
            box = r // 3 * 3 + c // 3
            for digit in range(1, 10):
                if digit in rows[r] or digit in cols[c] or digit in boxes[box]:
                    continue
                rows[r].add(digit)
                cols[c].add(digit)
                boxes[box].add(digit)
                board[r][c] = digit
                if fill(k + 1):
                    return True
                board[r][c] = 0
                rows[r].remove(digit)
                cols[c].remove(digit)
                boxes[box].remove(digit)
            return False

        return fill(0)
