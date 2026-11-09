# REFERENCE: d487 EPI 14.2 Find the first key greater than a given value in a BST
class Solution:
    def find_first_greater_than_k(self, tree, k):
        best, node = None, tree
        while node:
            if node.val > k:
                best, node = node, node.left
            else:
                node = node.right
        return best
