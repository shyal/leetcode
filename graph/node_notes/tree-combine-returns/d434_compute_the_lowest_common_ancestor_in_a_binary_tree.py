# REFERENCE: d434 EPI 9.3 Compute the lowest common ancestor in a binary tree
class Solution:
    def lca(self, tree, node0, node1):
        def search(node):
            if node is None or node is node0 or node is node1:
                return node
            left, right = search(node.left), search(node.right)
            return node if left and right else left or right

        return search(tree)
