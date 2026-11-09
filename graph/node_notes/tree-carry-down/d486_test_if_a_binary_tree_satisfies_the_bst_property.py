# REFERENCE: d486 EPI 14.1 Test if a binary tree satisfies the BST property
class Solution:
    def is_binary_tree_bst(self, tree):
        def within(node, low, high):
            if node is None:
                return True
            return low <= node.val <= high and within(node.left, low, node.val) and within(node.right, node.val, high)

        return within(tree, -inf, inf)
