# REFERENCE: d458 EPI 11.6 Search in a 2D sorted array
class Solution:
    def matrix_search(self, A, x):
        r, c = 0, len(A[0]) - 1 if A else -1
        while r < len(A) and c >= 0:
            if A[r][c] == x:
                return True
            if A[r][c] < x:
                r += 1
            else:
                c -= 1
        return False
