# REFERENCE: d340 Find The Duplicates
class Solution:
    def find_duplicates(self, arr1, arr2):
        i = j = 0
        out = []
        while i < len(arr1) and j < len(arr2):
            if arr1[i] < arr2[j]:
                i += 1
            elif arr1[i] > arr2[j]:
                j += 1
            else:
                out.append(arr1[i])
                i += 1
                j += 1
        return out
