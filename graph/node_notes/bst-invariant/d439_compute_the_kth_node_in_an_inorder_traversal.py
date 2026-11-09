# REFERENCE: d439 EPI 9.8 Compute the kth node in an inorder traversal
class Solution:
    def find_kth_node_binary_tree(self, tree, k):
        node = tree
        while node:
            left = node.left.size if node.left else 0
            if k <= left:
                node = node.left
            elif k == left + 1:
                return node
            else:
                k -= left + 1
                node = node.right
        return None
