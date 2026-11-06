# REFERENCE: d324 Absolute Value Sort
class Solution:
    def absSort(self, arr):
        return sorted(arr, key=lambda x: (abs(x), x))
