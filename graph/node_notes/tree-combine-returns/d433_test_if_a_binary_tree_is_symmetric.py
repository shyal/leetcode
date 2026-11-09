# REFERENCE: d433 EPI 9.2 Test if a binary tree is symmetric
class Solution:
    def is_symmetric(self, tree):
        def mirror(a, b):
            if a is None or b is None:
                return a is b
            return a.val == b.val and mirror(a.left, b.right) and mirror(a.right, b.left)

        return tree is None or mirror(tree.left, tree.right)
