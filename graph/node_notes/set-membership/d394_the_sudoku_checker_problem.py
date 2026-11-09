# REFERENCE: d394 EPI 5.17 The Sudoku checker problem
class Solution:
    def is_valid_sudoku(self, partial_assignment):
        seen = set()
        for i, row in enumerate(partial_assignment):
            for j, d in enumerate(row):
                if d:
                    for key in (("row", i, d), ("col", j, d), ("box", i // 3, j // 3, d)):
                        if key in seen:
                            return False
                        seen.add(key)
        return True
