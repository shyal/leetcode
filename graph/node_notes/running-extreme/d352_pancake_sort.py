# REFERENCE: d352 Pancake Sort
class Solution:
    def pancake_sort(self, arr):
        def flip(k):
            arr[: k + 1] = arr[k::-1]

        for end in range(len(arr) - 1, 0, -1):
            top = max(range(end + 1), key=lambda i: arr[i])
            flip(top)
            flip(end)
        return arr
