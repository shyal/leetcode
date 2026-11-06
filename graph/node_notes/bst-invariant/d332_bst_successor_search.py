# REFERENCE: d332 BST Successor Search
class Solution:
    def find_in_order_successor(self, root, inputNode):
        succ = None
        node = root
        while node:
            if node.val > inputNode.val:
                succ = node
                node = node.left
            else:
                node = node.right
        return succ
