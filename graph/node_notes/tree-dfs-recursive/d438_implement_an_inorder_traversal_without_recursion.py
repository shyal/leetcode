# REFERENCE: d438 EPI 9.7 Implement an inorder traversal without recursion
class Solution:
    def inorder_traversal(self, tree):
        out, stack, node = [], [], tree
        while stack or node:
            if node:
                stack.append(node)
                node = node.left
            else:
                node = stack.pop()
                out.append(node.val)
                node = node.right
        return out
