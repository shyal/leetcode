# REFERENCE: d346 Matrix Spiral Copy
class Solution:
    def spiral_copy(self, inputMatrix):
        top, bottom = 0, len(inputMatrix) - 1
        left, right = 0, len(inputMatrix[0]) - 1
        res = []
        while top <= bottom and left <= right:
            for c in range(left, right + 1):
                res.append(inputMatrix[top][c])
            top += 1
            for r in range(top, bottom + 1):
                res.append(inputMatrix[r][right])
            right -= 1
            if top <= bottom:
                for c in range(right, left - 1, -1):
                    res.append(inputMatrix[bottom][c])
                bottom -= 1
            if left <= right:
                for r in range(bottom, top - 1, -1):
                    res.append(inputMatrix[r][left])
                left += 1
        return res
