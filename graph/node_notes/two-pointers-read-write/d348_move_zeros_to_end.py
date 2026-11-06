# REFERENCE: d348 Move Zeros To End
class Solution:
    def moveZerosToEnd(self, arr):
        w = 0
        for x in arr:
            if x != 0:
                arr[w] = x
                w += 1
        for i in range(w, len(arr)):
            arr[i] = 0
        return arr
