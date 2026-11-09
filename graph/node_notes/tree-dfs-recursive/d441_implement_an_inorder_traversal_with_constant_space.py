# REFERENCE: d441 EPI 9.10 Implement an inorder traversal with constant space
class Solution:
    def inorder_traversal(self, tree):
        out, prev, node = [], None, tree
        while node:
            if prev is node.parent:
                if node.left:
                    prev, node = node, node.left
                    continue
                out.append(node.val)
                prev, node = node, node.right or node.parent
            elif prev is node.left:
                out.append(node.val)
                prev, node = node, node.right or node.parent
            else:
                prev, node = node, node.parent
        return out
