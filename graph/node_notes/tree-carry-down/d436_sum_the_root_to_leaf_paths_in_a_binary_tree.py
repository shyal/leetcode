# REFERENCE: d436 EPI 9.5 Sum the root-to-leaf paths in a binary tree
class Solution:
    def sum_root_to_leaf(self, tree):
        def total(node, prefix):
            if node is None:
                return 0
            prefix = 2 * prefix + node.val
            if node.left is None and node.right is None:
                return prefix
            return total(node.left, prefix) + total(node.right, prefix)

        return total(tree, 0)
