# REFERENCE: d428 EPI 8.6 Compute binary tree nodes in order of increasing depth
class Solution:
    def binary_tree_depth_order(self, tree):
        out, level = [], [tree] if tree else []
        while level:
            out.append([node.val for node in level])
            level = [kid for node in level for kid in (node.left, node.right) if kid]
        return out
