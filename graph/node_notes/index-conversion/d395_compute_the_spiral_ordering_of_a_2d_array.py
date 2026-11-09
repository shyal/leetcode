# REFERENCE: d395 EPI 5.18 Compute the spiral ordering of a 2D array
class Solution:
    def matrix_in_spiral_order(self, square_matrix):
        res = []
        lo, hi = 0, len(square_matrix) - 1
        while lo < hi:
            res += [square_matrix[lo][j] for j in range(lo, hi)]
            res += [square_matrix[i][hi] for i in range(lo, hi)]
            res += [square_matrix[hi][j] for j in range(hi, lo, -1)]
            res += [square_matrix[i][lo] for i in range(hi, lo, -1)]
            lo += 1
            hi -= 1
        if lo == hi:
            res.append(square_matrix[lo][lo])
        return res
