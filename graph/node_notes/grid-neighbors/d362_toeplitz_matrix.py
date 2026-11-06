# REFERENCE: d362 Toeplitz Matrix
class Solution:
    def isToeplitz(self, arr):
        return all(
            arr[r][c] == arr[r - 1][c - 1]
            for r in range(1, len(arr))
            for c in range(1, len(arr[0]))
        )
