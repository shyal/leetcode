# REFERENCE: d445 EPI 9.14 Compute the exterior of a binary tree
class Solution:
    def exterior_binary_tree(self, tree):
        def is_leaf(node):
            return node.left is None and node.right is None

        def left_side(node, edge):
            if node is None:
                return []
            here = [node] if edge or is_leaf(node) else []
            return here + left_side(node.left, edge) + left_side(node.right, edge and node.left is None)

        def right_side(node, edge):
            if node is None:
                return []
            here = [node] if edge or is_leaf(node) else []
            return right_side(node.left, edge and node.right is None) + right_side(node.right, edge) + here

        if tree is None:
            return []
        if is_leaf(tree):
            return [tree]
        return [tree] + left_side(tree.left, True) + right_side(tree.right, True)
