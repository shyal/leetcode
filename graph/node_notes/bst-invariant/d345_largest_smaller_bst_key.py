# REFERENCE: d345 Largest Smaller BST Key
class Solution:
    def find_largest_smaller_key(self, rootNode, num):
        result = -1
        node = rootNode
        while node is not None:
            if node.val < num:
                result = node.val
                node = node.right
            else:
                node = node.left
        return result
