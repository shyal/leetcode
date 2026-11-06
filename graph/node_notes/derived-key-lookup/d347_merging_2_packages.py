# REFERENCE: d347 Merging 2 Packages
class Solution:
    def get_indices_of_item_weights(self, arr, limit):
        seen = {}
        for i, w in enumerate(arr):
            if limit - w in seen:
                return [i, seen[limit - w]]
            seen[w] = i
        return []
