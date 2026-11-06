# REFERENCE: d326 Array of Array Products
class Solution:
    def array_of_array_products(self, arr):
        if len(arr) < 2:
            return []
        products = [1] * len(arr)
        before = 1
        for i in range(len(arr)):
            products[i] = before
            before *= arr[i]
        after = 1
        for i in range(len(arr) - 1, -1, -1):
            products[i] *= after
            after *= arr[i]
        return products
