# REFERENCE: d443 EPI 9.12 Reconstruct a binary tree from a preorder traversal with markers
class Solution:
    def reconstruct_preorder(self, preorder):
        values = iter(preorder)

        def build():
            val = next(values)
            if val is None:
                return None
            left = build()
            return TreeNode(val, left, build())

        return build()
