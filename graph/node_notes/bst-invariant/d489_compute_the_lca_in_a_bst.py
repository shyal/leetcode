# REFERENCE: d489 EPI 14.4 Compute the LCA in a BST
class Solution:
    def find_lca(self, tree, s, b):
        node = tree
        while not s.val <= node.val <= b.val:
            node = node.left if b.val < node.val else node.right
        return node
