# REFERENCE: d444 EPI 9.13 Compute the leaves of a binary tree
class Solution:
    def create_list_of_leaves(self, tree):
        if tree is None:
            return []
        if tree.left is None and tree.right is None:
            return [tree]
        return self.create_list_of_leaves(tree.left) + self.create_list_of_leaves(tree.right)
