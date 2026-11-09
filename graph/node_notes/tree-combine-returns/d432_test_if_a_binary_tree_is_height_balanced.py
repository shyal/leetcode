# REFERENCE: d432 EPI 9.1 Test if a binary tree is height-balanced
class Solution:
    def is_balanced_binary_tree(self, tree):
        def height(node):
            if node is None:
                return 0
            left, right = height(node.left), height(node.right)
            if left < 0 or right < 0 or abs(left - right) > 1:
                return -1
            return 1 + max(left, right)

        return height(tree) >= 0
