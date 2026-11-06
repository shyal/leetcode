# REFERENCE: d351 Pairs with Specific Difference
class Solution:
    def find_pairs_with_given_difference(self, arr, k):
        if k == 0:
            return []
        have = set(arr)
        return [[y + k, y] for y in arr if y + k in have]
