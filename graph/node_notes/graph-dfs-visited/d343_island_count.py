# REFERENCE: d343 Island Count
class Solution:
    def get_number_of_islands(self, binaryMatrix):
        rows, cols = len(binaryMatrix), len(binaryMatrix[0])

        def sink(i, j):
            stack = [(i, j)]
            while stack:
                r, c = stack.pop()
                if 0 <= r < rows and 0 <= c < cols and binaryMatrix[r][c] == 1:
                    binaryMatrix[r][c] = 0
                    stack += [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]

        islands = 0
        for i in range(rows):
            for j in range(cols):
                if binaryMatrix[i][j] == 1:
                    sink(i, j)
                    islands += 1
        return islands
