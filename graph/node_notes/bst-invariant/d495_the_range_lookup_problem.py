# REFERENCE: d495 EPI 14.10 The range lookup problem
class Solution:
    def range_lookup_in_bst(self, tree, interval):
        left, right = interval
        out = []

        def walk(node):
            if node is None:
                return
            if left < node.val:
                walk(node.left)
            if left <= node.val <= right:
                out.append(node.val)
            if node.val < right:
                walk(node.right)

        walk(tree)
        return out
