# REFERENCE: d446 EPI 9.15 Compute the right sibling tree
class Solution:
    def construct_right_sibling(self, tree):
        if tree:
            tree.next = None
        level = tree
        while level and level.left:
            node = level
            while node:
                node.left.next = node.right
                node.right.next = node.next.left if node.next else None
                node = node.next
            level = level.left
