# REFERENCE: d437 EPI 9.6 Find a root to leaf path with specified sum
class Solution:
    def has_path_sum(self, tree, remaining_weight):
        if tree is None:
            return False
        remaining_weight -= tree.val
        if tree.left is None and tree.right is None:
            return remaining_weight == 0
        return self.has_path_sum(tree.left, remaining_weight) or self.has_path_sum(tree.right, remaining_weight)
